# Decisions

Newest first. What was decided, and why.

## 2026-10-28: Fixed data splits, set before any test
In sample 2015–2021 (ideas are built here), validation 2022–2023 (checked once per idea), holdout 2024 onward (touched only for a final verdict). Set in `nqlab/data.py` before any hypothesis exists. Moving them after seeing results would let the holdout leak into the research.

## 2026-10-28: Data cleaning rules
Duplicate bars are merged with volume summed. Sessions with broken data are dropped rather than repaired (9 sessions, all in 2025); real halts such as the March 2020 circuit breakers are kept. Contract rolls are not back-adjusted, because the source has only one contract at a time, so the true roll spread is unknown. Strategies that hold overnight must avoid `roll_window` sessions instead.

## 2026-10-28: Research is public, including failures
Hypotheses are committed before testing so timestamps prove the order. Rejected ideas stay in the repo; publishing only winners would create the survivorship bias this project is meant to avoid.
