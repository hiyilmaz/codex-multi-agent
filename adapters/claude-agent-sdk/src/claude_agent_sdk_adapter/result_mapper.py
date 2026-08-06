from dataclasses import dataclass
from typing import Any

from claude_agent_sdk import ResultMessage


@dataclass(frozen=True)
class QueryOutcome:
    status: str
    success: bool
    terminal_observed: bool = False
    subtype: str | None = None
    session_id: str | None = None
    result: str | None = None
    structured_output: Any = None
    errors: list[str] | None = None
    api_error_status: int | None = None
    terminal_reason: str | None = None
    total_cost_usd: float | None = None
    raw_usage: dict[str, Any] | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    cache_creation_input_tokens: int | None = None
    cache_read_input_tokens: int | None = None
    max_turns: int | None = None
    max_budget_usd: float | None = None
    elapsed_seconds: float = 0.0


def _token_value(usage: dict[str, Any] | None, key: str) -> int | None:
    if usage is None:
        return None
    value = usage.get(key)
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def map_messages(messages, *, max_turns, max_budget_usd, elapsed_seconds):
    terminals = [message for message in messages if isinstance(message, ResultMessage)]
    assistant_error = any(
        not isinstance(message, ResultMessage) and bool(getattr(message, "error", None))
        for message in messages
    )
    terminal = terminals[0] if terminals else None

    if assistant_error:
        status = "failed"
    elif len(terminals) != 1:
        status = "unverified"
    elif terminal.is_error or terminal.errors or terminal.api_error_status is not None:
        status = "failed"
    else:
        status = "passed"

    usage = terminal.usage if terminal is not None else None
    return QueryOutcome(
        status=status,
        success=status == "passed",
        terminal_observed=bool(terminals),
        subtype=terminal.subtype if terminal is not None else None,
        session_id=terminal.session_id if terminal is not None else None,
        result=terminal.result if terminal is not None else None,
        structured_output=terminal.structured_output if terminal is not None else None,
        errors=terminal.errors if terminal is not None else None,
        api_error_status=terminal.api_error_status if terminal is not None else None,
        terminal_reason=terminal.terminal_reason if terminal is not None else None,
        total_cost_usd=terminal.total_cost_usd if terminal is not None else None,
        raw_usage=usage,
        input_tokens=_token_value(usage, "input_tokens"),
        output_tokens=_token_value(usage, "output_tokens"),
        cache_creation_input_tokens=_token_value(usage, "cache_creation_input_tokens"),
        cache_read_input_tokens=_token_value(usage, "cache_read_input_tokens"),
        max_turns=max_turns,
        max_budget_usd=max_budget_usd,
        elapsed_seconds=elapsed_seconds,
    )
