# H-001 results: 15-minute opening range breakout

**Verdict: rejected at step 1 (in sample).** Validation and holdout data were not used, so they stay unseen for future hypotheses.

Run on 2026-10-28 with `python backtests/H-001-opening-range/h001.py in_sample`. The rules are exactly those committed in [`H-001`](../../hypotheses/H-001-opening-range-breakout.md) before this run, and the rule logic is unit-tested in `test_h001.py`.

## In sample, 2015–2021, after costs

| Measure | Value |
|:---|---:|
| Sessions | 1,807 |
| Trades | 1,775 |
| Win rate | 39.2% |
| Average win | 1.38R |
| Average loss | 0.91R |
| **Expectancy** | **−0.014R** |
| 95% bootstrap CI | −0.078R to +0.051R |
| Expectancy without the 10 best trades | −0.054R |
| Expectancy before costs | +0.024R |
| Max drawdown | 81.2R |
| Total | −25.0R |
| Trades stopped out | 49% |
| Median risk | 28 points |
| Median cost per trade | 0.03R |

The criterion was expectancy > 0R with the lower confidence bound > 0R. Neither holds, so the hypothesis is rejected.

## What the numbers say

- **There's no measurable edge before costs either.** +0.024R per trade before costs is well inside noise. Costs are small (about 0.03R, because the range is wide), so this wasn't killed by costs. There was simply nothing there.
- **Win rate alone would mislead.** Wins average 1.5 times the size of losses, but only 39% of trades win. That's the pattern from the expectancy example on the profile, and here it nets out to roughly zero.
- **The drawdown is large.** An 81R drawdown with no edge is what a random walk with a 1R stop looks like over 1,775 trades.

## Breakdown (reported, not used to rescue the result)

| Group | Trades | Win rate | Avg win R | Avg loss R | Expectancy R | 95% CI |
|:---|---:|---:|---:|---:|---:|:---:|
| All | 1775 | 39.2% | 1.38 | 0.91 | −0.014 | [−0.078, +0.051] |
| Long | 924 | 43.6% | 1.27 | 0.91 | +0.041 | [−0.043, +0.125] |
| Short | 851 | 34.4% | 1.53 | 0.92 | −0.074 | [−0.169, +0.031] |
| 2015 | 255 | 34.9% | 1.45 | 0.97 | −0.127 | [−0.288, +0.041] |
| 2016 | 255 | 36.5% | 1.47 | 0.92 | −0.044 | [−0.217, +0.143] |
| 2017 | 253 | 37.9% | 1.26 | 0.88 | −0.071 | [−0.241, +0.118] |
| 2018 | 256 | 34.8% | 1.82 | 0.89 | +0.051 | [−0.133, +0.249] |
| 2019 | 247 | 40.9% | 1.30 | 0.89 | +0.006 | [−0.153, +0.166] |
| 2020 | 252 | 39.7% | 1.32 | 0.95 | −0.045 | [−0.202, +0.120] |
| 2021 | 257 | 49.8% | 1.16 | 0.90 | +0.130 | [−0.014, +0.280] |
| Before 2020 | 1266 | 37.0% | 1.45 | 0.91 | −0.037 | [−0.115, +0.043] |
| 2020 on | 509 | 44.8% | 1.23 | 0.92 | +0.043 | [−0.065, +0.153] |
| Narrow range | 585 | 36.6% | 1.74 | 0.98 | +0.016 | [−0.113, +0.151] |
| Middle range | 586 | 40.8% | 1.26 | 0.91 | −0.023 | [−0.124, +0.078] |
| Wide range | 584 | 39.9% | 1.19 | 0.85 | −0.039 | [−0.136, +0.061] |
| Roll window | 190 | 36.3% | 1.32 | 0.92 | −0.109 | [−0.292, +0.090] |
| Outside roll window | 1585 | 39.6% | 1.39 | 0.91 | −0.003 | [−0.071, +0.065] |

**Every group's confidence interval includes zero.** That's 17 comparisons; at 95% confidence, about one would look "significant" by chance even with no edge anywhere. Longs doing better than shorts fits a market that rose for most of 2015–2021, which is a market drift, not a breakout edge.

**Don't mine this table.** "Long only" or "2021-style years only" are ideas suggested by this very data. Testing either on the same in-sample period would be circular. If one becomes a new hypothesis, its first honest test is the validation period, and it must be written down before that test.
