---
name: crypto-strategy-discovery
description: Discover and evaluate signal-strategy candidates from realized crypto market, trade, or backtest data. Use when Codex is asked to analyze historical/realized crypto data, find strategy ideas for a signal bot, design leakage-safe research plans, compare accepted and rejected candidates, or produce evidence-based strategy discovery reports before implementation.
---

# Crypto Strategy Discovery

## Purpose

Use this skill to run a discovery-first workflow for signal strategies using realized crypto data. Keep the work separate from production runtime until the user explicitly approves implementation.

This skill is for research, filtering, and reporting. It is not for deploying strategies, changing live bot behavior, or connecting lab code to production services.

## Operating Rules

- Treat realized data as evidence, not proof of future performance.
- Preserve uncertainty. Use `tespit edilemedi` or an English equivalent in written reports when evidence is missing.
- Do not use future-derived fields as model features or entry filters.
- Do not connect to production runtime, live trading systems, or exchange accounts unless the user explicitly approves that separate task.
- Move from discovery to strategy building only after explicit user approval.
- Save reports in the project-appropriate research/report directory when one exists; otherwise ask before creating a new artifact path.

## Workflow

1. Define the research target.
   Identify symbols, market type, timeframe, signal horizon, allowed directions, transaction-cost assumptions, and the definition of a successful signal.

2. Inventory available data.
   Separate market candles/order book data, generated signals, accepted trades, rejected candidates, diagnostics, and realized outcomes. Record gaps before analysis.

3. Build a leakage-safe dataset plan.
   Exclude fields that would only be known after entry decision time: realized PnL, exit price, bars held, TP/SL hit results, optimizer score derived from outcome, and any post-entry labels.

4. Generate candidate hypotheses.
   Prefer testable ideas with a clear market behavior premise, entry trigger, invalidation logic, risk model, and expected failure mode.

5. Evaluate candidates with gates.
   Check sample size, out-of-sample behavior, regime separation, transaction costs, slippage/spread, liquidity, parameter sensitivity, and normal/inverse symmetry where relevant.

6. Classify results.
   Label each candidate as `PROMISING`, `NEEDS_MORE_DATA`, `REJECTED`, or `INSUFFICIENT_EVIDENCE`. Include rejection stage and rejection reason.

7. Report before implementation.
   Produce a concise report with data sources, assumptions, candidate table, evidence, risks, and the next approval decision. Do not implement the strategy in bot code during discovery.

## Minimum Candidate Record

Each candidate should have:

- `candidate_id`
- `strategy_name`
- `market_premise`
- `symbols` and `timeframes`
- `entry_conditions`
- `exit_or_invalidation_conditions`
- `risk_model`
- `required_features`
- `forbidden_leakage_fields_checked`
- `sample_size`
- `in_sample_result`
- `out_of_sample_result`
- `regime_notes`
- `cost_model`
- `decision`
- `rejection_reason` when rejected
- `implementation_readiness`

## Evaluation Gates

Use these gates before calling any strategy promising:

- Enough independent trades or candidate events for the target timeframe.
- No single narrow period explains most of the edge.
- Performance survives realistic fees, spread, slippage, and latency assumptions.
- Parameters are stable across nearby values.
- Long and short behavior is analyzed separately when both are possible.
- Out-of-sample or walk-forward evidence exists.
- Failure cases are documented, not hidden.

## Report Shape

Use this structure for discovery reports unless the project provides a stricter template:

```text
# Strategy Discovery Report

## Scope
## Data Sources
## Leakage Controls
## Candidate Summary
## Candidate Details
## Rejected Ideas
## Risks and Unknowns
## Recommendation
## Approval Needed
```

## Handoff To Builder

Only hand off to a strategy-building workflow after the user approves a specific candidate. The handoff must include candidate ID, exact entry/exit rules, required features, risk settings, diagnostics to log, and verification criteria.
