import asyncio
import inspect
import math
import unittest

from helpers import (
    ADAPTER_ROOT,
    BlockingAsyncIterator,
    BlockingCloseAsyncIterator,
    ClosableAsyncIterator,
    RecordingQuery,
    result_message,
)
from claude_agent_sdk_adapter.runner import QueryRequest, run_query
from claude_agent_sdk_adapter.sessions import SessionSpec
from claude_agent_sdk import query as sdk_query


class RunnerTests(unittest.IsolatedAsyncioTestCase):
    async def test_calls_query_once_with_exact_request_and_options(self):
        stream = ClosableAsyncIterator([result_message(result="alpha")])
        query = RecordingQuery(stream)
        request = QueryRequest(
            prompt="first prompt",
            timeout_seconds=2,
            max_turns=3,
            max_budget_usd=0.3,
            session=SessionSpec(resume="11111111-1111-4111-8111-111111111111", fork_session=True),
        )
        outcome = await run_query(request, query_fn=query)
        self.assertEqual(outcome.result, "alpha")
        self.assertEqual(len(query.calls), 1)
        prompt, options = query.calls[0]
        self.assertEqual(prompt, request.prompt)
        self.assertEqual(options.max_turns, 3)
        self.assertEqual(options.max_budget_usd, 0.3)
        self.assertEqual(options.resume, request.session.resume)
        self.assertTrue(options.fork_session)
        self.assertTrue(stream.closed)

    async def test_rejects_invalid_bounds_before_query(self):
        invalid = (
            {"prompt": ""},
            {"prompt": "x" * 65537},
            {"prompt": "ok", "timeout_seconds": 0},
            {"prompt": "ok", "timeout_seconds": math.inf},
            {"prompt": "ok", "timeout_seconds": 301},
            {"prompt": "ok", "max_turns": 0},
            {"prompt": "ok", "max_turns": 11},
            {"prompt": "ok", "max_budget_usd": 0},
            {"prompt": "ok", "max_budget_usd": 1.01},
        )
        for values in invalid:
            query = RecordingQuery(ClosableAsyncIterator([]))
            with self.subTest(values=values), self.assertRaises(ValueError):
                await run_query(QueryRequest(**values), query_fn=query)
            self.assertEqual(query.calls, [])

    async def test_accepts_exact_boundaries(self):
        for request in (
            QueryRequest(prompt="x", timeout_seconds=0.001, max_turns=1, max_budget_usd=0.001),
            QueryRequest(prompt="x" * 65536, timeout_seconds=300, max_turns=10, max_budget_usd=1),
        ):
            query = RecordingQuery(ClosableAsyncIterator([result_message()]))
            outcome = await run_query(request, query_fn=query)
            self.assertTrue(outcome.success)

    async def test_exception_missing_and_duplicate_never_retry(self):
        cases = (
            (ClosableAsyncIterator([], RuntimeError("sdk failed")), "failed"),
            (ClosableAsyncIterator([]), "unverified"),
            (ClosableAsyncIterator([result_message(), result_message()]), "unverified"),
        )
        for stream, status in cases:
            query = RecordingQuery(stream)
            outcome = await run_query(QueryRequest(prompt="test"), query_fn=query)
            self.assertEqual(outcome.status, status)
            self.assertFalse(outcome.success)
            self.assertEqual(len(query.calls), 1)
            self.assertTrue(stream.closed)

    async def test_pre_cancel_never_calls_query(self):
        event = asyncio.Event()
        event.set()
        query = RecordingQuery(ClosableAsyncIterator([result_message()]))
        outcome = await run_query(QueryRequest(prompt="test"), cancel_event=event, query_fn=query)
        self.assertEqual(outcome.status, "not_executed")
        self.assertFalse(outcome.success)
        self.assertEqual(query.calls, [])

    async def test_live_sdk_boundary_is_default_denied(self):
        self.assertIsNone(inspect.signature(run_query).parameters["query_fn"].default)
        for values in ({}, {"query_fn": sdk_query}):
            with self.subTest(values=values):
                outcome = await run_query(QueryRequest(prompt="must not leave process"), **values)
                self.assertEqual(outcome.status, "not_executed")
                self.assertFalse(outcome.success)
                self.assertEqual(outcome.terminal_reason, "live_api_not_authorized")

    async def test_in_flight_cancel_and_timeout_close(self):
        cancel_stream = BlockingAsyncIterator()
        cancel_event = asyncio.Event()
        task = asyncio.create_task(
            run_query(QueryRequest(prompt="test", timeout_seconds=1), cancel_event=cancel_event, query_fn=RecordingQuery(cancel_stream))
        )
        await cancel_stream.entered.wait()
        cancel_event.set()
        outcome = await task
        self.assertEqual(outcome.status, "failed")
        self.assertEqual(outcome.terminal_reason, "cancelled")
        self.assertTrue(cancel_stream.closed)

        timeout_stream = BlockingAsyncIterator()
        outcome = await run_query(
            QueryRequest(prompt="test", timeout_seconds=0.001),
            query_fn=RecordingQuery(timeout_stream),
        )
        self.assertEqual(outcome.status, "failed")
        self.assertEqual(outcome.terminal_reason, "timeout")
        self.assertTrue(timeout_stream.closed)

    async def test_external_task_cancellation_closes_and_reraises(self):
        stream = BlockingAsyncIterator()
        task = asyncio.create_task(
            run_query(QueryRequest(prompt="test"), query_fn=RecordingQuery(stream))
        )
        await stream.entered.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertTrue(stream.closed)

    async def test_external_cancellation_during_final_close_is_reraised(self):
        stream = BlockingCloseAsyncIterator([result_message()])
        task = asyncio.create_task(
            run_query(QueryRequest(prompt="test"), query_fn=RecordingQuery(stream))
        )
        await stream.close_entered.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task


if __name__ == "__main__":
    unittest.main()
