# Chapter 3. H-003: overnight drift

**Repo:** [nq-h003-overnight-drift](https://github.com/nqedgelab/nq-h003-overnight-drift) · **Written and tested:** 2026-11-01 · **Verdict:** rejected in validation

## Why this one
H-002 showed that a 30-minute trade on NQ can't overcome its costs without a large effect. An overnight hold moves far more than its 1 bp round trip, so costs would no longer decide the result. The claim also has strong published evidence. Cliff, Cooper and Gulen (2008) and Lou, Polk and Skouras (*Journal of Financial Economics*, 2019) found that most US equity gains came between the close and the open.

## What was tested
Long at the 16:00 ET close, out at the 09:30 ET open of the next session. Nights with suspect data, roll weeks or missing sessions are skipped. To count, it had to make money after costs and also beat the next session's regular hours, 09:30 to 16:00.

## What happened
**In sample, 2015–2021: passed.** 1,523 nights, a 57.3% win rate and expectancy of **+5.20 bp**, with a 95% CI of +1.37 to +8.97 bp. Regular hours made +2.75 bp. This was the first idea in the book to pass step 1.

**Validation, 2022–2023: failed.** 433 nights, a 48.7% win rate and expectancy of **−2.14 bp**, with a 95% CI of −10.42 to +6.04 bp. Regular hours made +2.95 bp. It lost in the 2022 bear market (−6.40 bp). In 2023, a strong up year, overnight made only +2.17 bp against +11.58 bp for regular hours.

## What it means for the book
- **The process worked as designed.** An idea with an in-sample CI entirely above zero failed on data it hadn't seen. Without the validation period, it would have looked like the book's first edge.
- **Validation has now been seen.** 2022–2023 was used for the first time. Its shape is now known: a bear year, then a recovery year that rose in the day session. Any later idea built around the overnight or regular-hours split must say so in its "case against" section. Holdout is still untouched. This is recorded in [`decisions.md`](../decisions.md).
- **The best in-sample slices were the worst out of sample.** High-volatility nights fell from +13.64 bp to −6.47 bp, and nights after an up day from +7.79 bp to −7.27 bp. That's the clearest evidence so far for the "no mining the breakdowns" rule.
- **Benchmarks should compare like with like.** The overnight leg is 17.5 hours of trading against 6.5 for regular hours, so drift alone favoured it in step 2. Future benchmarks should match the holding time, or compare return per unit of risk.
- **A rising market makes long-only ideas look good.** Three ideas in, the only in-sample pass was long-only, in the strongest stretch of the sample. Future long-biased ideas should be expected to look better in sample than they are.
