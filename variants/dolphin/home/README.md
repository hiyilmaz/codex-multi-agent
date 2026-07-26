# DolphinVersion Agent Home

This directory is the DolphinVersion runtime-home template for:

```text
cognitivecomputations_dolphin-mistral-24b-venice-edition
```

Endpoint:

```text
https://lm.backstage8.com/v1/
```

It can be used in place through the source Dolphin launcher or installed as an
LLM runtime with:

```bash
bin/codex-user-install --variant dolphin
```

Prepare the environment from the repository root:

```bash
source variants/dolphin/bin/dolphin
```

After installation, use:

```bash
source ~/.llm-runtimes/dolphin/bin/llm-dolphin
```

The wrapper exports:

```text
AGENT_HOME=<runtime-home>
MODEL_API_BASE_URL=https://lm.backstage8.com/v1/
MODEL_ID=cognitivecomputations_dolphin-mistral-24b-venice-edition
```

The runtime includes `orchestration-gate` for project-level
`ORCHESTRATION_MODE` decisions:

```text
skip | ask-approval | run-chain
```

It must not bypass active tool or approval policy.

The runtime also includes the ECC `tdd-workflow` skill for mandatory test-first
feature, bugfix, and refactor work. The `tdd-guide` agent defines the focused
test strategy; `tdd-workflow` enforces the RED-GREEN-refactor loop.

Mandatory chain stages use bounded handoffs. Each stage consumes prior
evidence, avoids repeated discovery, and returns a concise result. Passing
tests alone do not prove completion; reviewers also check acceptance criteria,
observable behavior, and test integrity.
