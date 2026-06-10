# DolphinVersion

Isolated agent runtime variant for the remote LM-compatible endpoint at:

```text
https://lm.backstage8.com/v1/
```

Selected model:

```text
cognitivecomputations_dolphin-mistral-24b-venice-edition
```

This directory is intentionally separate from the repository root setup and
from any user-global agent home.

## Layout

```text
DolphinVersion/
  AGENTS.md
  bin/dolphin
  agent-home/
  docs/CHANGELOG.md
  docs/reports/
```

## Endpoint Check

The model list was checked with:

```bash
curl https://lm.backstage8.com/v1/models
```

The response included:

```text
cognitivecomputations_dolphin-mistral-24b-venice-edition
```

## Prepare Environment

To apply the environment to the current shell:

```bash
source DolphinVersion/bin/dolphin
```

To print the export commands without modifying the current shell:

```bash
DolphinVersion/bin/dolphin
```

The launcher prepares:

```text
AGENT_HOME=<repo>/DolphinVersion/agent-home
MODEL_API_BASE_URL=https://lm.backstage8.com/v1/
MODEL_ID=cognitivecomputations_dolphin-mistral-24b-venice-edition
```

It does not start any agent tool. Use these exported values with the tool you
choose later.
