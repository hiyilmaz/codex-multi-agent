import asyncio
import math
import time
from contextlib import suppress
from dataclasses import dataclass, field
from typing import Callable

from claude_agent_sdk import query as sdk_query

from .permissions import build_options
from .result_mapper import QueryOutcome, map_messages
from .sessions import SessionSpec


@dataclass(frozen=True)
class QueryRequest:
    prompt: str
    timeout_seconds: float = 30.0
    max_turns: int = 1
    max_budget_usd: float = 0.10
    session: SessionSpec = field(default_factory=SessionSpec)


def _validate_request(request: QueryRequest) -> None:
    if not isinstance(request.prompt, str) or not request.prompt:
        raise ValueError("prompt must be a non-empty string")
    try:
        prompt_size = len(request.prompt.encode("utf-8"))
    except UnicodeEncodeError as error:
        raise ValueError("prompt must be valid UTF-8") from error
    if prompt_size > 65_536:
        raise ValueError("prompt must not exceed 65536 UTF-8 bytes")
    if (
        isinstance(request.timeout_seconds, bool)
        or not isinstance(request.timeout_seconds, (int, float))
        or not math.isfinite(request.timeout_seconds)
        or not 0 < request.timeout_seconds <= 300
    ):
        raise ValueError("timeout_seconds must be finite and in (0, 300]")
    if isinstance(request.max_turns, bool) or not isinstance(request.max_turns, int) or not 1 <= request.max_turns <= 10:
        raise ValueError("max_turns must be an integer in [1, 10]")
    if (
        isinstance(request.max_budget_usd, bool)
        or not isinstance(request.max_budget_usd, (int, float))
        or not math.isfinite(request.max_budget_usd)
        or not 0 < request.max_budget_usd <= 1
    ):
        raise ValueError("max_budget_usd must be finite and in (0, 1]")


def _failure(
    request: QueryRequest,
    *,
    status: str,
    reason: str,
    elapsed_seconds: float,
    error: BaseException | None = None,
) -> QueryOutcome:
    return QueryOutcome(
        status=status,
        success=False,
        terminal_reason=reason,
        errors=[str(error)] if error is not None else None,
        max_turns=request.max_turns,
        max_budget_usd=request.max_budget_usd,
        elapsed_seconds=elapsed_seconds,
    )


async def _close_stream(stream) -> BaseException | None:
    close = getattr(stream, "aclose", None)
    if close is None:
        return None
    try:
        await close()
    except Exception as error:
        return error
    return None


async def run_query(
    request: QueryRequest,
    *,
    cancel_event: asyncio.Event | None = None,
    query_fn: Callable | None = None,
) -> QueryOutcome:
    _validate_request(request)
    options = build_options(request)
    started = time.monotonic()
    if cancel_event is not None and cancel_event.is_set():
        return _failure(
            request,
            status="not_executed",
            reason="cancelled_before_start",
            elapsed_seconds=time.monotonic() - started,
        )
    if query_fn is None or query_fn is sdk_query:
        return _failure(
            request,
            status="not_executed",
            reason="live_api_not_authorized",
            elapsed_seconds=time.monotonic() - started,
        )

    stream = None
    consume_task = None
    cancel_task = None
    messages = []
    failure_reason = None
    failure_error = None

    async def consume() -> None:
        async for message in stream:
            messages.append(message)

    try:
        stream = query_fn(prompt=request.prompt, options=options)
        consume_task = asyncio.create_task(consume())
        if cancel_event is None:
            await asyncio.wait_for(consume_task, timeout=request.timeout_seconds)
        else:
            cancel_task = asyncio.create_task(cancel_event.wait())
            done, _ = await asyncio.wait(
                {consume_task, cancel_task},
                timeout=request.timeout_seconds,
                return_when=asyncio.FIRST_COMPLETED,
            )
            if not done:
                failure_reason = "timeout"
            elif cancel_task in done and cancel_event.is_set():
                failure_reason = "cancelled"
            else:
                await consume_task
    except asyncio.TimeoutError:
        failure_reason = "timeout"
    except asyncio.CancelledError:
        if consume_task is not None:
            consume_task.cancel()
            with suppress(asyncio.CancelledError):
                await consume_task
        await _close_stream(stream)
        raise
    except Exception as error:
        failure_reason = "sdk_error"
        failure_error = error
    finally:
        if failure_reason is not None and consume_task is not None and not consume_task.done():
            consume_task.cancel()
            with suppress(asyncio.CancelledError):
                await consume_task
        if cancel_task is not None and not cancel_task.done():
            cancel_task.cancel()
            with suppress(asyncio.CancelledError):
                await cancel_task

    close_error = await _close_stream(stream)
    elapsed = time.monotonic() - started
    if close_error is not None and failure_error is None:
        failure_reason = "cleanup_error"
        failure_error = close_error
    if failure_reason is not None:
        return _failure(
            request,
            status="failed",
            reason=failure_reason,
            elapsed_seconds=elapsed,
            error=failure_error,
        )
    return map_messages(
        messages,
        max_turns=request.max_turns,
        max_budget_usd=request.max_budget_usd,
        elapsed_seconds=elapsed,
    )
