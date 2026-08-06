import unittest

from helpers import ADAPTER_ROOT  # noqa: F401
from claude_agent_sdk_adapter.sessions import SessionSpec, validate_session


SESSION_A = "11111111-1111-4111-8111-111111111111"
SESSION_B = "22222222-2222-4222-8222-222222222222"


class SessionTests(unittest.TestCase):
    def test_new_named_resume_and_fork_modes(self):
        self.assertEqual(validate_session(SessionSpec()), {})
        self.assertEqual(validate_session(SessionSpec(session_id=SESSION_A)), {"session_id": SESSION_A})
        self.assertEqual(validate_session(SessionSpec(resume=SESSION_A)), {"resume": SESSION_A})
        self.assertEqual(
            validate_session(SessionSpec(resume=SESSION_A, fork_session=True)),
            {"resume": SESSION_A, "fork_session": True},
        )

    def test_rejects_conflicts_and_fork_without_resume(self):
        with self.assertRaises(ValueError):
            validate_session(SessionSpec(session_id=SESSION_A, resume=SESSION_B))
        with self.assertRaises(ValueError):
            validate_session(SessionSpec(fork_session=True))

    def test_rejects_invalid_session_ids(self):
        for value in ("", "not-a-uuid", "11111111-1111-1111-1111-11111111111\n"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_session(SessionSpec(session_id=value))


if __name__ == "__main__":
    unittest.main()
