<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/banner-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/banner-light.svg" />
  <img src="./assets/banner-dark.svg" alt="nq-research: the lab notebook behind NQ Lab. Ideas tested: 1. Edges found: 0 so far." width="100%" />
</picture>

<br>

<div align="center">
  <img src="https://img.shields.io/badge/hypotheses-1-3b82f6?style=flat-square&labelColor=1e293b" alt="hypotheses: 1" />
  <img src="https://img.shields.io/badge/supported-0-22c55e?style=flat-square&labelColor=1e293b" alt="supported: 0" />
  <img src="https://img.shields.io/badge/rejected-1-ef4444?style=flat-square&labelColor=1e293b" alt="rejected: 1" />
  <img src="https://img.shields.io/badge/tests-21%20passing-14b8a6?style=flat-square&labelColor=1e293b" alt="tests: 21 passing" />
  <img src="https://img.shields.io/badge/data-NQ%201--min%202015%E2%80%932025-6366f1?style=flat-square&labelColor=1e293b" alt="data: NQ 1-minute, 2015 to 2025" />
  <img src="https://img.shields.io/badge/python-3.14-0ea5e9?style=flat-square&logo=python&logoColor=white&labelColor=1e293b" alt="python 3.14" />
</div>

<br>

Testing trading ideas on Nasdaq-100 E-mini (NQ) futures. Each idea is written down before it's tested, judged on expectancy after costs, and kept in the record whether it works or not.

> [!IMPORTANT]
> Paper trading only. Nothing here is financial advice, a signal, or a recommendation.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/section-record-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/section-record-light.svg" />
  <img src="./assets/section-record-dark.svg" alt="The research record" width="100%" />
</picture>

<div align="center">

| ID | Idea | Trades | Expectancy | 95% CI | Verdict |
|:---:|:---|:---:|:---:|:---:|:---:|
| [H-001](hypotheses/H-001-opening-range-breakout.md) | Opening range breakout | 1,775 | −0.014R | −0.08 to +0.05 | ![rejected](https://img.shields.io/badge/rejected-ef4444?style=flat-square) |

<sub>Expectancy is per trade, in sample, after costs.</sub>

</div>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/h001-equity-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/h001-equity-light.svg" />
  <img src="./assets/h001-equity-dark.svg" alt="H-001 cumulative result in sample: 1,775 trades from 2015 to 2021 ending at minus 25 R" width="100%" />
</picture>

**H-001, in short:** buying or selling the first break of the opening 15 minutes made +0.024R per trade before costs and −0.014R after, which is noise either way. It was rejected on the in-sample period, so the validation and holdout years were never used. [Full results →](backtests/H-001-opening-range/results.md)

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/section-process-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/section-process-light.svg" />
  <img src="./assets/section-process-dark.svg" alt="How an idea gets tested" width="100%" />
</picture>

```mermaid
flowchart LR
    A["Write it down"] --> B["In sample"]
    B --> C{"Positive?"}
    C -- No --> X["Rejected"]
    C -- Yes --> D["Validation"]
    D --> E{"Positive?"}
    E -- No --> X
    E -- Yes --> F["Holdout"]
    F --> G{"Positive?"}
    G -- No --> X
    G -- Yes --> H["Paper trade"]

    classDef step fill:#1e293b,stroke:#64748b,color:#f1f5f9
    classDef gate fill:#3b82f6,stroke:#1d4ed8,color:#ffffff
    classDef stop fill:#334155,stroke:#64748b,color:#cbd5e1
    class A,B,D,F,H step
    class C,E,G gate
    class X stop
```

1. **Write it down.** A file in [`hypotheses/`](hypotheses/) states the claim, the exact rules, the costs, and the result that would prove it wrong. It's committed before any test, so the timestamp shows the idea came first.
2. **Test it.** Code, unit tests for the rules, and a `results.md` go in [`backtests/`](backtests/), one folder per hypothesis.
3. **Pass every gate.** Expectancy has to stay above zero after costs in each period, and in sample the low end of the 95% confidence interval has to be above zero too.
4. **Paper trade survivors.** Simulated trades go in [`journal/trades.csv`](journal/trades.csv) in a fixed format, so live expectancy is measured rather than guessed.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/section-splits-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/section-splits-light.svg" />
  <img src="./assets/section-splits-dark.svg" alt="Three periods, fixed in advance" width="100%" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/splits-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/splits-light.svg" />
  <img src="./assets/splits-dark.svg" alt="In sample 2015 to 2021, 1,807 sessions. Validation 2022 to 2023, 517 sessions. Holdout 2024 to July 2025, 396 sessions." width="100%" />
</picture>

<br>

The periods were fixed before the first hypothesis existed and are recorded in [`decisions.md`](decisions.md). An idea that fails in sample never sees the later periods, so they stay clean for the ideas that come after it.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/section-data-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/section-data-light.svg" />
  <img src="./assets/section-data-dark.svg" alt="Data and setup" width="100%" />
</picture>

Every backtest loads bars through `nqlab.data`, so they all share the same cleaning rules.

```python
from nqlab import data

bars = data.load()                        # clean 1-minute bars in New York time
in_sample = data.split(bars, "in_sample")  # also "validation" and "holdout"
```

<div align="center">

| Column | Meaning |
|:---|:---|
| `open` `high` `low` `close` `volume` | The 1-minute bar |
| `session` | Trading date. The 18:00 ET open belongs to the next day. |
| `rth` | Regular hours, 09:30 to 16:00 ET |
| `roll_window` | Sessions around a quarterly contract roll |

</div>

<details>
<summary><b>What the cleaning does</b></summary>
<br>

- **Duplicates.** 112 timestamps appear twice, usually one bar with its volume split across two rows. They're merged and the volume is added.
- **Time zone.** The source is in UTC; everything is converted to New York time, including daylight saving.
- **Contract rolls.** Prices jump about 1% when the series switches to the next quarterly contract, and they aren't back-adjusted. Intraday strategies aren't affected. Anything held overnight must avoid `roll_window` sessions.
- **Broken sessions.** 9 sessions in 2025 with missing or mixed-contract data are dropped. The four March 2020 circuit-breaker halts are real market events and are kept.

`data.session_report()` shows the quality check for every session.

</details>

<details>
<summary><b>Setup</b></summary>
<br>

```bash
pip install -r requirements.txt
cp .env.example .env     # then set NQ_DATA_DIR to the folder with NQ_1min_<year>.parquet
python -m pytest
```

Market data isn't in the repo. It's licensed and can't be redistributed, and trade lists derived from it are git-ignored too.

</details>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/section-map-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/section-map-light.svg" />
  <img src="./assets/section-map-dark.svg" alt="What's in the repo" width="100%" />
</picture>

```
nq-research/
├── hypotheses/        one file per idea, written before it's tested
├── backtests/         code, rule tests and results for each hypothesis
├── nqlab/             shared code: the data loader and research splits
├── journal/           paper trades, once something survives
├── tests/             tests for the shared code
├── assets/            README artwork and the script that draws it
└── decisions.md       why the process works the way it does
```

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/section-rules-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/section-rules-light.svg" />
  <img src="./assets/section-rules-dark.svg" alt="House rules" width="100%" />
</picture>

- **Rules are frozen at the commit.** Changing a rule after seeing a result makes it a new hypothesis, with its own file.
- **Failures stay.** Deleting rejected ideas would leave only the lucky ones, which is survivorship bias.
- **No mining the breakdowns.** Results are split by year, direction and regime to understand them, never to rescue a failed idea.
- **Costs are always in.** Commission and slippage come off every trade, and stops that are run through by a gap fill at the open.
- **Every claim gets a falsification test.** If nothing could prove an idea wrong, it isn't ready to test.

<br>

<p align="center">
  <sub>Part of <a href="https://github.com/nqedgelab">NQ Lab</a> · paper traded · not financial advice</sub>
</p>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,100:3b82f6&height=90&section=footer" width="100%" alt="" />
