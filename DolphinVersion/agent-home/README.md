# DolphinVersion Agent Home

This directory is an isolated agent runtime home for:

```text
cognitivecomputations_dolphin-mistral-24b-venice-edition
```

Endpoint:

```text
https://lm.backstage8.com/v1/
```

It is not intended to be copied into or synchronized with any user-global agent
home.

Prepare the environment from the repository root:

```bash
source DolphinVersion/bin/dolphin
```

The wrapper exports:

```text
AGENT_HOME=<repo>/DolphinVersion/agent-home
MODEL_API_BASE_URL=https://lm.backstage8.com/v1/
MODEL_ID=cognitivecomputations_dolphin-mistral-24b-venice-edition
```
