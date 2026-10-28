# nq-research

Testing trading ideas on NQ (Nasdaq-100 E-mini) futures: written down first, tested second, kept whether they work or not.

> **Paper trading only. Not financial advice.** Nothing here is a signal or a recommendation.

## How this works

1. **Hypothesis first.** Every idea gets a file in [`hypotheses/`](hypotheses/) *before* it is tested: the claim, what would prove it wrong, and the sample size needed. The commit timestamp shows the idea came before the result.
2. **Test it.** Backtest code and results live in [`backtests/`](backtests/), each linked to its hypothesis.
3. **Paper trade survivors.** Simulated trades are logged in [`journal/trades.csv`](journal/trades.csv) in a fixed format so expectancy is calculated, not estimated.
4. **Record the verdict.** Supported, rejected, or inconclusive. Failures stay in the repo; deleting them would bias the record.

Decisions about process and rules are logged in [`decisions.md`](decisions.md).

## What's not here

- **Market data.** Exchange and vendor data can't be redistributed. Raw data lives in `data/`, which is git-ignored.
- **Secrets.** API keys go in `.env` (git-ignored). See `.env.example`.

## Contact

Questions or critiques are welcome. Open an issue.
