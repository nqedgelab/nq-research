"""H-001: 15-minute opening range breakout. Rules are in
hypotheses/H-001-opening-range-breakout.md and must not change here.

Usage: python backtests/H-001-opening-range/h001.py in_sample
"""

import sys
from datetime import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from nqlab import data  # noqa: E402

RANGE_START, RANGE_END = time(9, 30), time(9, 45)
SIGNAL_END = time(12, 0)
RANGE_BARS = 15

TICK = 0.25
COMMISSION = 0.25       # points per round trip ($2.50 per side at $20/point)
SLIP_ENTRY = 1 * TICK
SLIP_TIME_EXIT = 1 * TICK
SLIP_STOP_EXIT = 2 * TICK

# Which years of files each split needs, so a run never reads later data.
SPLIT_YEARS = {
    "in_sample": range(2015, 2022),
    "validation": range(2022, 2024),
    "holdout": range(2024, 2026),
}


def simulate_day(day: pd.DataFrame):
    """Return one trade dict for a session's regular-hours bars, or None."""
    clock = day.index.time
    opening = day[(clock >= RANGE_START) & (clock < RANGE_END)]
    if len(opening) != RANGE_BARS:
        return None
    high, low = opening["high"].max(), opening["low"].min()

    after = day[clock >= RANGE_END]
    window = after[after.index.time < SIGNAL_END]
    breaks = window[(window["close"] > high) | (window["close"] < low)]
    if breaks.empty:
        return None
    signal_time = breaks.index[0]
    side = 1 if breaks["close"].iloc[0] > high else -1
    stop = low if side == 1 else high

    rest = after[after.index > signal_time]
    if rest.empty:
        return None
    entry = rest["open"].iloc[0]
    risk = (entry - stop) * side
    if risk <= 0:
        return None

    exit_price, exit_time, stopped = rest["close"].iloc[-1], rest.index[-1], False
    for t, bar in rest.iterrows():
        adverse = bar["low"] if side == 1 else bar["high"]
        if (adverse - stop) * side <= 0:
            gapped = (bar["open"] - stop) * side <= 0
            exit_price, exit_time, stopped = (bar["open"] if gapped else stop), t, True
            break

    gross = (exit_price - entry) * side
    cost = COMMISSION + SLIP_ENTRY + (SLIP_STOP_EXIT if stopped else SLIP_TIME_EXIT)
    return {
        "session": day["session"].iloc[0], "side": side,
        "entry_time": rest.index[0], "exit_time": exit_time,
        "entry": entry, "stop": stop, "exit": exit_price, "stopped": stopped,
        "range_width": high - low, "risk_points": risk,
        "gross_points": gross, "cost_points": cost,
        "r": (gross - cost) / risk, "roll_window": bool(day["roll_window"].iloc[0]),
    }


def run(bars: pd.DataFrame) -> pd.DataFrame:
    rth = bars[bars["rth"]]
    trades, widths = [], {}
    for session, day in rth.groupby("session", sort=True):
        opening = day[(day.index.time >= RANGE_START) & (day.index.time < RANGE_END)]
        if len(opening) == RANGE_BARS:
            widths[session] = opening["high"].max() - opening["low"].min()
        trade = simulate_day(day)
        if trade:
            trades.append(trade)
    trades = pd.DataFrame(trades)

    # Range width relative to the median of the previous 20 sessions' ranges.
    width = pd.Series(widths)
    prior = width.rolling(20, min_periods=20).median().shift(1)
    trades["width_ratio"] = trades["session"].map(width / prior)
    return trades


def summarize(r: np.ndarray, seed: int = 1) -> dict:
    rng = np.random.default_rng(seed)
    boots = rng.choice(r, size=(10_000, len(r)), replace=True).mean(axis=1)
    equity = np.cumsum(r)
    drawdown = np.max(np.maximum.accumulate(np.concatenate([[0], equity]))[1:] - equity)
    wins, losses = r[r > 0], r[r <= 0]
    return {
        "trades": len(r),
        "win_rate": len(wins) / len(r),
        "avg_win_r": wins.mean() if len(wins) else 0.0,
        "avg_loss_r": -losses.mean() if len(losses) else 0.0,
        "expectancy_r": r.mean(),
        "ci_low": np.percentile(boots, 2.5),
        "ci_high": np.percentile(boots, 97.5),
        "max_drawdown_r": drawdown,
        "expectancy_without_top10": np.sort(r)[:-10].mean() if len(r) > 10 else np.nan,
        "total_r": r.sum(),
    }


def report(trades: pd.DataFrame) -> str:
    def row(name, sub):
        s = summarize(sub["r"].to_numpy())
        return (f"| {name} | {s['trades']} | {s['win_rate']:.1%} | {s['avg_win_r']:.2f} | "
                f"{s['avg_loss_r']:.2f} | {s['expectancy_r']:+.3f} | "
                f"[{s['ci_low']:+.3f}, {s['ci_high']:+.3f}] |")

    lines = ["| Group | Trades | Win rate | Avg win R | Avg loss R | Expectancy R | 95% CI |",
             "|:---|---:|---:|---:|---:|---:|:---:|", row("All", trades),
             row("Long", trades[trades.side == 1]), row("Short", trades[trades.side == -1])]
    years = pd.to_datetime(trades["session"]).dt.year
    for y in sorted(years.unique()):
        lines.append(row(str(y), trades[years == y]))
    lines.append(row("Before 2020", trades[years < 2020]))
    lines.append(row("2020 on", trades[years >= 2020]))
    w = trades.dropna(subset=["width_ratio"])
    cuts = w["width_ratio"].quantile([1 / 3, 2 / 3]).to_numpy()
    lines.append(row("Narrow range", w[w.width_ratio <= cuts[0]]))
    lines.append(row("Middle range", w[(w.width_ratio > cuts[0]) & (w.width_ratio <= cuts[1])]))
    lines.append(row("Wide range", w[w.width_ratio > cuts[1]]))
    lines.append(row("Roll window", trades[trades.roll_window]))
    lines.append(row("Outside roll window", trades[~trades.roll_window]))
    return "\n".join(lines)


def main(split_name: str) -> None:
    bars = data.split(data.load(years=SPLIT_YEARS[split_name]), split_name)
    trades = run(bars)
    out = Path(__file__).resolve().parent / f"trades_{split_name}.csv"
    trades.to_csv(out, index=False)

    s = summarize(trades["r"].to_numpy())
    gross = (trades["gross_points"] / trades["risk_points"]).mean()
    print(f"split: {split_name}  sessions: {bars['session'].nunique()}")
    for k, v in s.items():
        print(f"{k:>26}: {v:.4f}" if isinstance(v, float) else f"{k:>26}: {v}")
    print(f"{'expectancy_before_costs':>26}: {gross:.4f}")
    print(f"{'stopped_share':>26}: {trades['stopped'].mean():.4f}")
    print(f"{'median_risk_points':>26}: {trades['risk_points'].median():.2f}")
    print(f"{'median_cost_in_r':>26}: {(trades['cost_points'] / trades['risk_points']).median():.4f}")
    print()
    print(report(trades))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "in_sample")
