# Chapter 2. H-002: intraday momentum

**Repo:** [nq-h002-intraday-momentum](https://github.com/nqedgelab/nq-h002-intraday-momentum) · **Written and tested:** 2026-10-29 · **Verdict:** rejected in sample

## Why this one
H-001 was a well-known idea of our own choosing. H-002 tests someone else's published claim instead. Gao, Han, Li and Zhou ("Market Intraday Momentum", *Journal of Financial Economics*, 2018) reported that on SPY the first half hour's return predicts the last half hour's. Testing it on NQ is an out-of-sample test that our own data couldn't have shaped. It also answered two lessons from chapter 1: it has to beat simple drift, and its short trades would show whether costs bite.

## What was tested
The return from the previous 16:00 ET close to 10:00 ET sets the direction. The trade enters at 15:30 and exits at 16:00, long or short, with no stop. Roll weeks and early closes are skipped. There's no stop, so results are in basis points of the entry price, and the trade had to beat always-long on the same days as well as zero.

## What happened
In sample, 2015–2021: 1,520 trades and a 47.3% win rate. Expectancy was **−0.80 bp** after costs, with a 95% CI of −2.36 to +0.83 bp, and +0.34 bp before costs. The morning return and the last half hour had a correlation of 0.02. It lost money before the paper's publication as well as after, so this wasn't an edge that decayed once known.

## What it means for the book
- **Validation and holdout are still unseen.** Two ideas have now failed in sample, so both later periods remain clean.
- **Short trades need a big effect.** A 30-minute trade cost about 1.1 bp, three times the gross effect. Future short-horizon ideas should estimate their expected move against costs before they're written down.
- **Published results don't transfer automatically.** NQ futures keep trading past 16:00, so the closing flows behind the SPY result may not apply. The instrument's own structure belongs in the "why it might work" section.
- **Drift depends on the window.** The full day drifted up in H-001's tests; the last half hour drifted down here. A benchmark has to be measured on the same window as the trade.
- **Results can be in basis points.** Ideas without a stop are measured in basis points of entry, which keeps early and late years comparable. The record table now mixes R and bp, and each row says which.
