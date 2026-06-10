# DolphinVersion Agent Home

This directory is the DolphinVersion runtime-home template for:

```text
cognitivecomputations_dolphin-mistral-24b-venice-edition
```

Endpoint:

```text
https://lm.backstage8.com/v1/
```

It can be used in place through the Dolphin launcher or copied into a selected
Codex home with:

```bash
bin/codex-user-install --variant dolphin
```

Prepare the environment from the repository root:

```bash
source variants/dolphin/bin/dolphin
```

The wrapper exports:

```text
AGENT_HOME=<repo>/variants/dolphin/home
MODEL_API_BASE_URL=https://lm.backstage8.com/v1/
MODEL_ID=cognitivecomputations_dolphin-mistral-24b-venice-edition
```
