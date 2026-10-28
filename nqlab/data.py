"""Load and clean NQ 1-minute bars.

Raw files are NQ_1min_<year>.parquet with columns timestamp (UTC, naive,
bar open time), open, high, low, close, volume. The data never enters the
repo; point NQ_DATA_DIR at the folder (in .env or the environment).

What cleaning does, and why:
- Duplicate timestamps are merged (first open, max high, min low, last
  close, summed volume). Most duplicates are one bar with its volume split
  across two rows.
- Time is converted to New York, so session rules read like the exchange.
- Each bar gets a `session` date. The CME session opens at 18:00 ET and
  belongs to the next day, so Sunday 18:00 is part of Monday's session.
- Contract rolls are NOT back-adjusted in the source. Prices jump about
  1% at the roll. `roll_window` marks the sessions where that can happen,
  so a strategy can avoid holding positions across them.
- Sessions with broken data are flagged `suspect` and dropped by default.
"""

import os
from datetime import date, time, timedelta
from pathlib import Path

import pandas as pd

TZ = "America/New_York"
RTH_START = time(9, 30)
RTH_END = time(16, 0)

# Longest run of missing minutes allowed inside regular hours before a
# session counts as broken. Real sessions rarely skip more than a minute.
MAX_RTH_GAP_MINUTES = 5

# Sessions checked by hand and found broken, with the reason.
KNOWN_BAD_SESSIONS = {
    date(2025, 2, 13): "no data for the whole day",
    date(2025, 2, 14): "follows a missing day; opens with a gap",
    **{date(2025, 6, d): "June 2025 roll: missing evenings, mixed contracts"
       for d in (13, 16, 17, 18, 19, 20)},
}

# Real trading halts. The gap is the market, not the data, so these
# sessions are kept.
KNOWN_HALTS = {
    date(2020, 3, 9): "market-wide circuit breaker",
    date(2020, 3, 12): "market-wide circuit breaker",
    date(2020, 3, 16): "market-wide circuit breaker",
    date(2020, 3, 18): "market-wide circuit breaker",
}

# Fixed before any hypothesis is tested. Changing these after seeing
# results would leak the holdout into the research.
SPLITS = {
    "in_sample": (date(2015, 1, 1), date(2021, 12, 31)),
    "validation": (date(2022, 1, 1), date(2023, 12, 31)),
    "holdout": (date(2024, 1, 1), date(2025, 12, 31)),
}


def data_dir() -> Path:
    """Return NQ_DATA_DIR from the environment or the repo's .env file."""
    value = os.environ.get("NQ_DATA_DIR")
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if not value and env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            key, _, rest = line.partition("=")
            if key.strip() == "NQ_DATA_DIR":
                value = rest.strip().strip('"')
    if not value:
        raise RuntimeError("Set NQ_DATA_DIR in .env to the folder with NQ_1min_*.parquet")
    return Path(value)


def load_raw(years=None, folder=None) -> pd.DataFrame:
    """Read the raw parquet files for the given years (all by default)."""
    folder = Path(folder) if folder else data_dir()
    files = sorted(folder.glob("NQ_1min_*.parquet"))
    if years is not None:
        wanted = {f"NQ_1min_{y}.parquet" for y in years}
        files = [f for f in files if f.name in wanted]
    if not files:
        raise FileNotFoundError(f"No NQ_1min_*.parquet files found in {folder}")
    return pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)


def clean(raw: pd.DataFrame) -> pd.DataFrame:
    """Merge duplicates, convert to New York time and add session columns."""
    df = (raw.sort_values("timestamp", kind="stable")
             .groupby("timestamp", sort=True)
             .agg(open=("open", "first"), high=("high", "max"),
                  low=("low", "min"), close=("close", "last"),
                  volume=("volume", "sum")))
    df.index = df.index.tz_localize("UTC").tz_convert(TZ)
    df.index.name = "time"

    df["session"] = (df.index + timedelta(hours=6)).date
    clock = df.index.time
    df["rth"] = (clock >= RTH_START) & (clock < RTH_END)
    df["roll_window"] = pd.Series(df["session"]).map(in_roll_window).to_numpy()
    return df


def third_friday(year: int, month: int) -> date:
    first = date(year, month, 1)
    return first + timedelta(days=(4 - first.weekday()) % 7 + 14)


def in_roll_window(day: date) -> bool:
    """True from the Thursday 8 days before quarterly expiry to expiry day.

    The CME convention rolls on that Thursday; this data often rolls later,
    in expiry week. The window covers both.
    """
    if day.month not in (3, 6, 9, 12):
        return False
    expiry = third_friday(day.year, day.month)
    return expiry - timedelta(days=8) <= day <= expiry


def session_report(df: pd.DataFrame) -> pd.DataFrame:
    """One row per session: bar counts, the longest RTH gap, and a verdict."""
    rth = df[df["rth"]]
    minutes = pd.Series(rth.index.as_unit("s").asi8 // 60, index=rth.index)
    gaps = minutes.groupby(rth["session"]).diff() - 1

    report = pd.DataFrame({
        "bars": df.groupby("session").size(),
        "rth_bars": rth.groupby("session").size(),
        "rth_max_gap": gaps.groupby(rth["session"]).max(),
    })
    report["rth_bars"] = report["rth_bars"].fillna(0).astype(int)
    report["rth_max_gap"] = report["rth_max_gap"].fillna(0).astype(int)

    reason = pd.Series("", index=report.index, dtype=object)
    halted = report.index.isin(list(KNOWN_HALTS))
    reason[(report["rth_max_gap"] > MAX_RTH_GAP_MINUTES) & ~halted] = "gap inside regular hours"
    for day, why in KNOWN_BAD_SESSIONS.items():
        if day in reason.index:
            reason[day] = why
    report["suspect"] = reason != ""
    report["reason"] = reason
    report.index.name = "session"
    return report


def load(years=None, folder=None, drop_suspect=True) -> pd.DataFrame:
    """Load clean NQ bars, indexed by New York time.

    Columns: open, high, low, close, volume, session, rth, roll_window.
    Suspect sessions are dropped unless drop_suspect is False.
    """
    df = clean(load_raw(years, folder))
    if drop_suspect:
        report = session_report(df)
        bad = set(report.index[report["suspect"]])
        df = df[~df["session"].isin(bad)]
    return df


def split(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Return the rows of one fixed research split, by session date."""
    start, end = SPLITS[name]
    sessions = df["session"]
    return df[(sessions >= start) & (sessions <= end)]
