from datetime import date

import pandas as pd
import pytest

from nqlab import data


def bars(*rows):
    """Build raw bars from (utc_timestamp, open, high, low, close, volume)."""
    df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def rth_day(day, skip=()):
    """A full 09:30-16:00 ET session on a summer day (ET = UTC-4)."""
    times = pd.date_range(f"{day} 13:30", f"{day} 19:59", freq="min")
    rows = [(t, 100.0, 101.0, 99.0, 100.5, 10) for i, t in enumerate(times) if i not in skip]
    return bars(*rows)


def test_duplicate_timestamps_are_merged_with_volume_summed():
    raw = bars(("2024-07-01 14:00", 100, 102, 99, 101, 30),
               ("2024-07-01 14:00", 100, 101, 98, 100, 15))
    df = data.clean(raw)
    assert len(df) == 1
    row = df.iloc[0]
    assert (row.open, row.high, row.low, row.close, row.volume) == (100, 102, 98, 100, 45)


def test_times_are_new_york_and_rth_follows_dst():
    # 13:30 UTC is 09:30 ET in summer and 08:30 ET in winter.
    df = data.clean(bars(("2024-07-01 13:30", 1, 1, 1, 1, 1),
                         ("2024-01-02 13:30", 1, 1, 1, 1, 1)))
    assert str(df.index.tz) == "America/New_York"
    assert df["rth"].tolist() == [False, True]


def test_evening_bars_belong_to_the_next_session():
    # Sunday 18:00 ET opens Monday's session; Monday 16:59 ET still belongs to it.
    df = data.clean(bars(("2024-06-30 22:00", 1, 1, 1, 1, 1),
                         ("2024-07-01 20:59", 1, 1, 1, 1, 1)))
    assert df["session"].tolist() == [date(2024, 7, 1), date(2024, 7, 1)]


@pytest.mark.parametrize("day, expected", [
    (date(2024, 3, 6), False),   # 9 days before March expiry
    (date(2024, 3, 7), True),    # CME roll Thursday
    (date(2024, 3, 15), True),   # expiry Friday
    (date(2024, 3, 18), False),
    (date(2024, 4, 11), False),  # not a quarterly month
])
def test_roll_window(day, expected):
    assert data.in_roll_window(day) is expected


def test_full_session_passes_and_gappy_session_is_suspect():
    good = rth_day("2024-07-01")
    gappy = rth_day("2024-07-02", skip=range(100, 110))
    report = data.session_report(data.clean(pd.concat([good, gappy])))
    assert report.loc[date(2024, 7, 1), "rth_bars"] == 390
    assert not report.loc[date(2024, 7, 1), "suspect"]
    assert report.loc[date(2024, 7, 2), "rth_max_gap"] == 10
    assert report.loc[date(2024, 7, 2), "suspect"]


def test_known_halts_are_not_suspect():
    # 2020-03-09 was a circuit-breaker day; ET = UTC-4 after the DST change.
    report = data.session_report(data.clean(rth_day("2020-03-09", skip=range(5, 20))))
    assert report.loc[date(2020, 3, 9), "rth_max_gap"] == 15
    assert not report.loc[date(2020, 3, 9), "suspect"]


def test_known_bad_sessions_are_flagged():
    report = data.session_report(data.clean(rth_day("2025-06-20")))
    assert report.loc[date(2025, 6, 20), "suspect"]


def test_load_drops_suspect_sessions(tmp_path):
    pd.concat([rth_day("2024-07-01"), rth_day("2024-07-02", skip=range(100, 110))]) \
        .to_parquet(tmp_path / "NQ_1min_2024.parquet")
    df = data.load(folder=tmp_path)
    assert set(df["session"]) == {date(2024, 7, 1)}
    assert len(data.load(folder=tmp_path, drop_suspect=False)) == 390 + 380


def test_splits_do_not_overlap_and_are_in_order():
    ranges = list(data.SPLITS.values())
    for (_, end), (start, _) in zip(ranges, ranges[1:]):
        assert end < start
