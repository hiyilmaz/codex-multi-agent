# Evidence - DolphinVersion

## Task

Create and update an isolated DolphinVersion runtime variant for
`cognitivecomputations_dolphin-mistral-24b-venice-edition`.

## Current Endpoint

```text
https://lm.backstage8.com/v1/
```

## Model Discovery

Command:

```bash
curl --silent --show-error --fail --max-time 10 https://lm.backstage8.com/v1/models
```

Relevant response entry:

```json
{
  "id": "cognitivecomputations_dolphin-mistral-24b-venice-edition",
  "object": "model",
  "owned_by": "organization_owner"
}
```

## Implementation Evidence

Results:

- Working directory was verified before changes.
- `AGENT_HOME` is the runtime root variable.
- `MODEL_API_BASE_URL` is `https://lm.backstage8.com/v1/`.
- `MODEL_ID` is
  `cognitivecomputations_dolphin-mistral-24b-venice-edition`.
- Launcher path is `variants/dolphin/bin/dolphin`.
- Runtime home is `variants/dolphin/home`.
- The launcher prepares environment variables only; it does not start a CLI.
- Forbidden legacy names were checked after the update and no file path matches
  remained under `variants/dolphin/`.
- Bash syntax validation passed for `variants/dolphin/bin/dolphin`.
- Execute mode prints export commands only.
- zsh source mode sets `AGENT_HOME`, `MODEL_API_BASE_URL`, and `MODEL_ID`.
