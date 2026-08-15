import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "bin/codex-user-install"
POLICIES = (
    "GLOBAL_AGENTS_TEMPLATE.md",
    "variants/codex/home/AGENTS.md",
    "variants/claude/home/CLAUDE.md",
    "variants/opencode/home/AGENTS.md",
)


class TaskTransitionGateTests(unittest.TestCase):
    def assert_task_transition_gate(self, text: str) -> None:
        normalized = " ".join(text.split())
        required = (
            "### Task Transition Gate",
            "Treat each distinct task as a hard stop",
            "never begin the next task automatically after completing the current one",
            "summarize the completed task in one or two short, clear sentences",
            "State the next known task and explain it briefly",
            "If no next task is known, say so explicitly",
            "Ask for explicit user approval before starting that next task, and wait",
            "Approval for the completed task never authorizes the next distinct task",
            "Steps that are already part of one explicitly approved task remain within that task",
        )
        for marker in required:
            self.assertIn(" ".join(marker.split()), normalized)

        forbidden = (
            "ask again between every step",
            "ask for approval between every step",
            "ask for approval before every step",
            "ask for explicit user approval before each step",
            "wait for approval between each step",
        )
        lowered = normalized.lower()
        for marker in forbidden:
            self.assertNotIn(marker, lowered)

    def test_all_canonical_policies_define_the_complete_gate(self) -> None:
        self.assertEqual(len(POLICIES), 4)
        self.assertIn("variants/opencode/home/AGENTS.md", POLICIES)
        for relative in POLICIES:
            with self.subTest(path=relative):
                self.assert_task_transition_gate(
                    (REPO_ROOT / relative).read_text(encoding="utf-8")
                )

    def test_partial_or_every_step_gate_is_rejected(self) -> None:
        partial = (
            "### Task Transition Gate\n"
            "Ask for explicit user approval before starting the next task, and wait.\n"
        )
        with self.assertRaises(AssertionError):
            self.assert_task_transition_gate(partial)

        contradictory = (REPO_ROOT / POLICIES[0]).read_text(encoding="utf-8")
        contradictory += "\nAsk again between every step of the current task.\n"
        with self.assertRaises(AssertionError):
            self.assert_task_transition_gate(contradictory)

    def test_portable_installs_expose_the_complete_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            environment = {**os.environ, "HOME": str(root / "home")}
            for variant in ("codex", "claude", "opencode"):
                runtime = root / variant
                result = subprocess.run(
                    (
                        str(INSTALLER),
                        "--runtime-home",
                        str(runtime),
                        "--variant",
                        variant,
                        "--force",
                    ),
                    cwd=REPO_ROOT,
                    env=environment,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                with self.subTest(variant=variant):
                    self.assertEqual(result.returncode, 0, result.stderr)
                    policy = "CLAUDE.md" if variant == "claude" else "AGENTS.md"
                    self.assert_task_transition_gate(
                        (runtime / policy).read_text(encoding="utf-8")
                    )

    def test_user_guides_explain_the_task_boundary(self) -> None:
        english = ("README.md", "USAGE_GUIDE.md", "COMMAND_REFERENCE.md")
        for relative in english:
            text = (REPO_ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                self.assertIn("Task Transition Gate", text)
                self.assertIn("next distinct task", text)
                self.assertIn("explicit approval", text)
                self.assertIn("same explicitly approved bounded task", text)

        turkish = (REPO_ROOT / "TURKCE_KURULUM_REHBERI.md").read_text(
            encoding="utf-8"
        )
        turkish = " ".join(turkish.split())
        for marker in (
            "Görev Geçiş Kapısı",
            "sıradaki farklı göreve",
            "açık kullanıcı onayı",
            "aynı açıkça onaylanmış sınırlı görevin",
        ):
            self.assertIn(marker, turkish)


if __name__ == "__main__":
    unittest.main()
