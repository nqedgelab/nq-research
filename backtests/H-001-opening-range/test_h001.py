import pandas as pd
import pytest

import h001


def day(prices, start="2024-07-01 09:30", session="2024-07-01"):
    """Build an RTH session from (open, high, low, close) bars, one per minute."""
    index = pd.date_range(start, periods=len(prices), freq="min", tz="America/New_York")
    df = pd.DataFrame(prices, columns=["open", "high", "low", "close"], index=index)
    df["volume"] = 10
    df["session"] = pd.Timestamp(session).date()
    df["rth"] = True
    df["roll_window"] = False
    return df


RANGE = [(100, 101, 99, 100)] * 15   # range high 101, low 99, width 2


def test_long_breakout_held_to_close():
    bars = RANGE + [(100, 101.5, 100, 101.5),   # 09:45 closes above 101: long signal
                    (102, 103, 101.5, 102.5),   # entry at 102
                    (102.5, 106, 102, 105)]     # last bar: exit at close 105
    t = h001.simulate_day(day(bars))
    assert (t["side"], t["entry"], t["stop"], t["exit"], t["stopped"]) == (1, 102, 99, 105, False)
    assert t["risk_points"] == 3
    cost = h001.COMMISSION + h001.SLIP_ENTRY + h001.SLIP_TIME_EXIT
    assert t["r"] == pytest.approx((3 - cost) / 3)


def test_short_stopped_out_at_stop_price():
    bars = RANGE + [(99.5, 99.5, 98, 98.5),     # closes below 99: short signal
                    (98.5, 99, 98, 98.5),       # entry at 98.5, stop 101
                    (99, 101.5, 98.75, 101)]    # trades through 101: stopped at 101
    t = h001.simulate_day(day(bars))
    assert (t["side"], t["entry"], t["exit"], t["stopped"]) == (-1, 98.5, 101, True)
    cost = h001.COMMISSION + h001.SLIP_ENTRY + h001.SLIP_STOP_EXIT
    assert t["r"] == pytest.approx((-2.5 - cost) / 2.5)


def test_gap_through_stop_exits_at_open():
    bars = RANGE + [(100, 101.5, 100, 101.5), (102, 102, 101.5, 102),
                    (97, 98, 96, 97)]           # opens below the 99 stop
    t = h001.simulate_day(day(bars))
    assert t["exit"] == 97 and t["stopped"]


def test_stop_checked_on_entry_bar():
    bars = RANGE + [(100, 101.5, 100, 101.5), (102, 102.5, 98.5, 99.5), (100, 100, 100, 100)]
    t = h001.simulate_day(day(bars))
    assert t["exit"] == 99 and t["stopped"]


def test_wick_outside_range_is_not_a_signal():
    bars = RANGE + [(100, 103, 98, 100)] * 10    # wicks both ways, closes inside
    assert h001.simulate_day(day(bars)) is None


def test_no_trade_when_break_comes_after_noon():
    inside = [(100, 100.5, 99.5, 100)] * (150 - 15)   # 09:45 to 11:59
    bars = RANGE + inside + [(100, 102, 100, 102), (102, 102, 102, 102)]
    assert h001.simulate_day(day(bars)) is None


def test_missing_range_bar_skips_the_day():
    d = day(RANGE + [(100, 102, 100, 102), (102, 102, 102, 102)])
    assert h001.simulate_day(d.drop(d.index[3])) is None


def test_only_first_signal_counts():
    bars = RANGE + [(100, 100, 98, 98.5),        # short signal first
                    (98.5, 98.5, 98, 98),        # entry 98.5
                    (98, 102, 98, 101.5),        # stopped at 101
                    (101.5, 103, 101.5, 103)]    # a long break afterwards is ignored
    t = h001.simulate_day(day(bars))
    assert t["side"] == -1
