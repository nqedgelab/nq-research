# H-001: 15-minute opening range breakout

- **Status:** rejected <!-- untested | testing | supported | rejected | inconclusive -->
- **Written:** 2026-10-28 (before any testing)

The data has been inspected for quality only (gaps, duplicates, rolls). No returns, breakouts or other trading statistics have been looked at.

## Claim
On NQ, trading in the direction of the first 1-minute close outside the 09:30–09:45 ET range, with the stop at the other side of the range and a fixed exit at the end of the session, has positive expectancy after costs.

## Why it might work
The first 15 minutes absorb overnight news and opening orders. A break of that range may show that one side still has orders to fill, and large orders get worked over hours, not minutes. On trend days the move continues long after the break. The other side is traders fading the move, plus short-term liquidity providers who are run over on those days.

**The case against.** This is one of the oldest and best-known day-trading setups, so any edge has had decades to be traded away. Index futures often revert intraday, and false breaks are common. The stop is wide by design (the full range), so wins must come from a few large trend days, and a handful of outliers could drive the whole result. Published versions of this idea suffer from the same selection problem this project exists to avoid. **The most likely outcome is expectancy near zero after costs.**

## Rules
All times New York (ET). Bars come from `nqlab.data.load()`, which drops sessions with broken data.

1. **Range.** The opening range is the high and low of the 15 one-minute bars from 09:30 to 09:44. If any of those bars is missing, skip the day.
2. **Signal.** From the 09:45 bar until the 11:59 bar, the first bar that **closes** above the range high is a long signal; the first that closes below the range low is a short signal. Only the first signal of the day counts, at most one trade per day. No signal by 12:00 means no trade.
3. **Entry.** At the open of the bar after the signal bar.
4. **Stop.** The other side of the range: the range low for longs, the range high for shorts. It's checked from the entry bar on. If a bar trades through the stop, the exit is at the stop price, or at that bar's open if it opened beyond the stop (a gap).
5. **Exit.** If the stop isn't hit, exit at the close of the last regular-hours bar of the session. That's normally 15:59; on early-close days it's earlier.
6. **Risk.** 1R = |entry − stop| in points. Results are measured in R, so position size doesn't affect them. The size is fixed at 1 contract and never changes.
7. **No filters.** There's no profit target, trailing stop, volatility filter, day-of-week rule or trend filter. Any variant, such as a 5- or 30-minute range or a target, is a new hypothesis with its own file, and it counts as another test.

## Falsification
H-001 is **rejected** if any of these holds, checked in order:

1. In sample (2015–2021), expectancy after costs is ≤ 0R, or the lower bound of its 95% bootstrap confidence interval is ≤ 0R.
2. Validation (2022–2023, looked at once), expectancy after costs is ≤ 0R.
3. Holdout (2024 onward, looked at once, only if 1 and 2 pass), expectancy after costs is ≤ 0R.

It's **supported** only if all three pass. It's **inconclusive** if any period has fewer than the minimum number of trades below.

A result that depends on a handful of days is fragile even if it passes. The test reports expectancy with the 10 best trades removed. If that turns negative, the verdict says so.

## Test plan
- **Data period.** The fixed splits in `nqlab/data.py`: in sample 2015–2021, validation 2022–2023, holdout 2024 to Jul 2025. Rules are frozen at this commit and can't be changed after seeing any result.
- **Minimum sample size.** 300 trades in sample and 100 each in validation and holdout. With about one signal per trading day, all three should be met easily.
- **Costs assumed.**
  - Commission and fees: $2.50 per side, or 0.25 points per round trip ($20 per point).
  - Slippage: 1 tick (0.25 points) on entry and on the time exit, 2 ticks (0.50 points) on stop exits.
  - Costs are charged in points and then converted to R, so narrow-range days cost more R. That's intended.
- **Regimes to check separately** (reported, not used to rescue a failed result):
  - longs vs shorts;
  - each calendar year;
  - range width tercile, measured against the previous 20 sessions;
  - before and after 2020;
  - roll-window sessions vs the rest.
- **Reported:** trade count, win rate, average win and loss in R, expectancy in R, its bootstrap 95% CI, max drawdown in R, and expectancy without the top 10 trades.

## Result
**Rejected at step 1** (tested 2026-10-28). In sample, after costs: 1,775 trades, 39.2% win rate, expectancy **−0.014R** (95% CI −0.078R to +0.051R), and +0.024R before costs. Validation and holdout were not used.

Full results: [`backtests/H-001-opening-range/results.md`](../backtests/H-001-opening-range/results.md).
