# Chapter 1. H-001: the opening range breakout

**Repo:** [nq-h001-opening-range](https://github.com/nqedgelab/nq-h001-opening-range) · **Written and tested:** 2026-10-28 · **Verdict:** rejected in sample

## Why start here
The opening range breakout is one of the oldest day-trading setups, and it's simple enough to code with no discretion. That made it a good first test of the whole process, from data loading to a verdict, with a well-known idea whose likely answer was "nothing there".

## What was tested
After 09:45 ET, trade in the direction of the first 1-minute close outside the 09:30–09:45 range, before noon. The stop goes at the other side of the range and the trade exits at the end of the session. Costs are included, there are no filters, and it's one trade a day.

## What happened
In sample, 2015–2021: 1,775 trades and a 39.2% win rate. Expectancy was **−0.014R** after costs, with a 95% CI of −0.078R to +0.051R, and +0.024R before costs. Every breakdown, by direction, year, range width and roll week, had a confidence interval that included zero.

## What it means for the book
- **Validation and holdout are still unseen.** The next hypothesis gets a clean first test on them.
- **Costs are small relative to wide stops.** At a median risk of 28 points they were about 0.03R a trade. Ideas with tight stops will feel costs much more.
- **Longs beat shorts in a rising market.** Any directional idea needs to beat simple drift, not just zero. That's worth stating as a benchmark in future hypotheses.
- **The loader and the rule tests worked.** The same pattern of one test per trading rule carries over to the next repo.
