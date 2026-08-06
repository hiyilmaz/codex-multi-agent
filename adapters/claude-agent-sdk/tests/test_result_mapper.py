import unittest
from types import SimpleNamespace

from helpers import ADAPTER_ROOT, result_message  # noqa: F401
from claude_agent_sdk_adapter.result_mapper import map_messages


class ResultMapperTests(unittest.TestCase):
    def test_single_non_error_terminal_is_the_only_pass(self):
        outcome = map_messages([result_message()], max_turns=2, max_budget_usd=0.2, elapsed_seconds=0.1)
        self.assertEqual(outcome.status, "passed")
        self.assertTrue(outcome.success)
        self.assertTrue(outcome.terminal_observed)

    def test_error_missing_duplicate_and_assistant_error_fail_closed(self):
        cases = (
            ([result_message(is_error=True, subtype="error")], "failed"),
            ([result_message(errors=["provider error"])], "failed"),
            ([result_message(api_error_status=503)], "failed"),
            ([], "unverified"),
            ([result_message(), result_message(session_id="22222222-2222-4222-8222-222222222222")], "unverified"),
            ([SimpleNamespace(error="rate_limit"), result_message()], "failed"),
        )
        for messages, status in cases:
            with self.subTest(status=status):
                outcome = map_messages(messages, max_turns=1, max_budget_usd=0.1, elapsed_seconds=0.1)
                self.assertEqual(outcome.status, status)
                self.assertFalse(outcome.success)

    def test_assistant_error_without_terminal_is_failed(self):
        outcome = map_messages(
            [SimpleNamespace(error="authentication_failed")],
            max_turns=1,
            max_budget_usd=0.1,
            elapsed_seconds=0.1,
        )
        self.assertEqual(outcome.status, "failed")
        self.assertFalse(outcome.success)
        self.assertFalse(outcome.terminal_observed)

    def test_preserves_metadata_and_normalizes_usage(self):
        terminal = result_message()
        outcome = map_messages([terminal], max_turns=4, max_budget_usd=0.4, elapsed_seconds=0.25)
        self.assertEqual(outcome.session_id, terminal.session_id)
        self.assertEqual(outcome.result, "done")
        self.assertEqual(outcome.structured_output, {"ok": True})
        self.assertEqual(outcome.total_cost_usd, 0.01)
        self.assertEqual(outcome.raw_usage["future_key"], 7)
        self.assertEqual(outcome.input_tokens, 10)
        self.assertEqual(outcome.output_tokens, 5)
        self.assertEqual(outcome.cache_creation_input_tokens, 2)
        self.assertEqual(outcome.cache_read_input_tokens, 3)
        self.assertEqual(outcome.max_turns, 4)
        self.assertEqual(outcome.max_budget_usd, 0.4)
        self.assertEqual(outcome.terminal_reason, "completed")

    def test_preserves_explicit_api_error_metadata(self):
        outcome = map_messages(
            [result_message(errors=["provider error"], api_error_status=503)],
            max_turns=1,
            max_budget_usd=0.1,
            elapsed_seconds=0.1,
        )
        self.assertEqual(outcome.status, "failed")
        self.assertEqual(outcome.errors, ["provider error"])
        self.assertEqual(outcome.api_error_status, 503)

    def test_missing_usage_and_cost_remain_unknown(self):
        outcome = map_messages(
            [result_message(usage=None, total_cost_usd=None)],
            max_turns=1,
            max_budget_usd=0.1,
            elapsed_seconds=0.1,
        )
        self.assertIsNone(outcome.raw_usage)
        self.assertIsNone(outcome.input_tokens)
        self.assertIsNone(outcome.total_cost_usd)


if __name__ == "__main__":
    unittest.main()
