from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str = ""
    stderr: str = ""


class ProcessRunner:
    """Runs fixed command vectors without a shell and without logging secrets."""

    def run(self, command: Sequence[str], *, env: Mapping[str, str] | None = None, timeout: int = 30) -> CommandResult:
        safe_env = os.environ.copy()
        if env:
            safe_env.update(env)
        try:
            result = subprocess.run(
                list(command), capture_output=True, text=True, check=False,
                env=safe_env, timeout=timeout, shell=False,
            )
            return CommandResult(result.returncode, result.stdout, result.stderr)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return CommandResult(124, "", exc.__class__.__name__)

    def run_with_input(self, command: Sequence[str], secret_input: str, *, timeout: int = 30) -> CommandResult:
        try:
            result = subprocess.run(list(command), input=secret_input, capture_output=True, text=True, check=False, timeout=timeout, shell=False)
            return CommandResult(result.returncode, result.stdout, result.stderr)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return CommandResult(124, "", exc.__class__.__name__)
