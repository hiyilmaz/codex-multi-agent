# Claude Agent SDK Adapter

This optional adapter provides a bounded Python integration for the Claude Agent
SDK without changing the project's native Claude configuration variant.

## Scope

- Pins `claude-agent-sdk==0.2.130` and records the complete resolution in
  `uv.lock`.
- Exposes no built-in tools, MCP servers, or Claude settings sources.
- Uses `dontAsk` permission mode and an explicit built-in tool denylist.
- Supports new, resumed, and forked sessions with validated UUID identifiers.
- Preserves terminal result, structured output, usage, token, cost, session, and
  configured budget metadata.
- Performs one SDK query attempt. It does not retry automatically.

`allowed_tools` is an approval mechanism, not a security sandbox. The adapter
therefore combines an empty tool surface with the denylist and empty settings
sources. A hosted deployment still needs operating-system and network isolation.

## Local Setup

Python 3.10 or newer and `uv` are required.

```bash
cd adapters/claude-agent-sdk
uv sync --frozen
```

The dependency must remain exactly pinned. Upgrade it deliberately by changing
`pyproject.toml`, regenerating `uv.lock`, reviewing the SDK API and transitive
dependency diff, and rerunning all adapter and project tests.

## Tests

```bash
cd adapters/claude-agent-sdk
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src uv run --frozen python -m unittest discover -s tests -p 'test_*.py' -v
```

The test suite uses injected in-memory streams. It does not read credentials or
make a real Claude API request.

## Programmatic Contract

Create a `QueryRequest` and pass it to the asynchronous `run_query` function.
Requests are bounded to 65,536 UTF-8 prompt bytes, 300 seconds, 10 turns, and a
configured maximum budget of USD 1. Session resume and fork identifiers must be
canonical UUID strings.

The Phase 5 adapter is offline by default. Calling `run_query` without an
injected transport, or explicitly passing the SDK's live `query` function,
returns `not_executed/live_api_not_authorized`. The `query_fn` injection point
exists for controlled offline transports and tests; it is not a live-API
authorization mechanism.

The returned `QueryOutcome.status` uses these values:

- `passed`: exactly one non-error terminal SDK result was observed.
- `failed`: the SDK reported an error, the request timed out or was cancelled,
  cleanup failed, or the stream raised an exception.
- `unverified`: the stream did not provide exactly one terminal SDK result.
- `not_executed`: cancellation was already requested before SDK invocation.

Only `passed` sets `success=True`. A configured `max_budget_usd` is an observable
client limit; it must not be treated as proof of a provider billing guarantee.

## Real API Gate

No real API smoke test is part of the local pilot. Before any credential-backed
call, obtain separate approval for the credential source, maximum cost, prompt,
expected result, and evidence handling. Gate C must add a separate live
executor with a per-call authorization capability, an isolated workspace and
Claude configuration directory, and a child process with a minimal allowlisted
environment. Never commit Claude credentials or captured sensitive responses.
