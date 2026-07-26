# Orchestration Chain Review

**Date:** 2026-07-26 04:52 +03
**Scope:** Read-only review; no runtime, chain, model, or agent changes.

## Result

The current chain is safe but unnecessarily expensive as a default:

```text
planner -> tdd-guide -> code-reviewer -> security-reviewer
```

All four active Codex roles pin `gpt-5.6-sol` with `high` reasoning, and the
registry requires sequential completion once orchestration starts.

## Main Findings

1. `high` is excessive as the default for planning, test selection, and routine
   code review. `medium` is the better baseline; escalate only for concrete
   complexity or risk.
2. The larger delay comes from four mandatory sequential stages. Changing only
   reasoning effort will help, but will not remove coordination and waiting
   overhead.
3. `planner` overlaps with main-agent discovery and planning.
4. `tdd-guide` overlaps with the active `tdd-workflow` skill and should focus
   only on non-obvious verification gaps.
5. `code-reviewer` is valuable for non-trivial diffs, but should not be required
   for routine mechanical work.
6. `security-reviewer` is valuable for security-sensitive changes, but running
   it for every orchestrated task adds low-value latency.
7. Independent correctness and security reviews can run in parallel when both
   are required.

## Research Summary

OpenAI documentation says subagents consume more tokens because each agent does
its own model and tool work. It recommends parallel agents mainly for
independent read-heavy work, warns about coordination overhead, and states that
higher reasoning increases response time and token use. It presents `medium`
for lighter agents and `high` for complex reviewer or security work.

Recent community reports consistently describe slow waits and increased usage
with broad subagent use. These reports are practical signals, not authoritative
product guarantees. OpenAI repository discussions also state that concurrent
agent consumption generally scales with the number of agents.

## Recommendation

- Use `medium` as the default for all four Codex roles.
- Escalate individual roles to `high` only when the task requires it.
- Make orchestration risk-based instead of always running the full chain.
- Run independent reviewers in parallel.
- Use EXPERIMENT records only after failure, uncertainty, regression, or a need
  for measured comparison.
- Benchmark before changing the protected global chain.

## Sources

- OpenAI Codex: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- OpenAI Codex: [Best practices](https://learn.chatgpt.com/docs/codex/best-practices)
- OpenAI Codex issue:
  [Subagent usage scaling](https://github.com/openai/codex/issues/9748)
- OpenAI Codex issue:
  [Parent-child wait behavior](https://github.com/openai/codex/issues/16900)
- OpenAI Codex issue:
  [Subagent routing controls](https://github.com/openai/codex/issues/31814)
- Reddit:
  [Slow subagent reports](https://www.reddit.com/r/codex/comments/1v1ak3f/codex_and_super_slow_subagents/)
- Reddit:
  [Review overhead discussion](https://www.reddit.com/r/OpenaiCodex/comments/1ugrp6f/codex_subagents_are_really_impressive_and_ig/)
