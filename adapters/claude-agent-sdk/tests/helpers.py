import asyncio
import sys
from pathlib import Path
from typing import Any


ADAPTER_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ADAPTER_ROOT / "src"))


class ClosableAsyncIterator:
    def __init__(self, messages: list[Any], error: BaseException | None = None):
        self.messages = iter(messages)
        self.error = error
        self.closed = False
        self.aclose_calls = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.messages)
        except StopIteration:
            if self.error is not None:
                error, self.error = self.error, None
                raise error
            raise StopAsyncIteration

    async def aclose(self):
        self.aclose_calls += 1
        self.closed = True


class BlockingAsyncIterator:
    def __init__(self):
        self.entered = asyncio.Event()
        self.release = asyncio.Event()
        self.closed = False
        self.aclose_calls = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        self.entered.set()
        await self.release.wait()
        raise StopAsyncIteration

    async def aclose(self):
        self.aclose_calls += 1
        self.closed = True
        self.release.set()


class BlockingCloseAsyncIterator(ClosableAsyncIterator):
    def __init__(self, messages: list[Any]):
        super().__init__(messages)
        self.close_entered = asyncio.Event()
        self.close_release = asyncio.Event()

    async def aclose(self):
        self.aclose_calls += 1
        self.close_entered.set()
        await self.close_release.wait()
        self.closed = True


class RecordingQuery:
    def __init__(self, stream):
        self.stream = stream
        self.calls = []

    def __call__(self, *, prompt, options):
        self.calls.append((prompt, options))
        if len(self.calls) > 1:
            raise AssertionError("query must not retry")
        return self.stream


def result_message(**overrides):
    from claude_agent_sdk import ResultMessage

    values = {
        "subtype": "success",
        "duration_ms": 10,
        "duration_api_ms": 8,
        "is_error": False,
        "num_turns": 1,
        "session_id": "11111111-1111-4111-8111-111111111111",
        "total_cost_usd": 0.01,
        "usage": {
            "input_tokens": 10,
            "output_tokens": 5,
            "cache_creation_input_tokens": 2,
            "cache_read_input_tokens": 3,
            "future_key": 7,
        },
        "result": "done",
        "structured_output": {"ok": True},
        "errors": None,
        "terminal_reason": "completed",
    }
    values.update(overrides)
    return ResultMessage(**values)
