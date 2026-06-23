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
