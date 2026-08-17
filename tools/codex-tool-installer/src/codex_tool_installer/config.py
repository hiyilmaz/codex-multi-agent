from __future__ import annotations

import os
import re
import shutil
import stat
import tempfile
from pathlib import Path
from typing import Callable, MutableSequence

try:
    import tomllib
except ImportError:  # pragma: no cover - Python 3.10 test-host compatibility
    import tomli as tomllib

from .models import TransactionResult


class ConfigError(RuntimeError):
    pass


class ConfigCollision(ConfigError):
    pass


class ConfigTransactionError(ConfigError):
    pass


_HEADER = re.compile(r"(?m)^[ \t]*\[([^\]\r\n]+)\][ \t]*(?:#.*)?(?:\r?\n|$)")
_MANAGED_MARKER = "# Managed by codex-tool-installer"


def _reject_symlinked_ancestors(path: Path) -> None:
    absolute = path.absolute()
    for candidate in reversed((absolute, *absolute.parents)):
        try:
            mode = os.lstat(candidate).st_mode
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(mode):
            if candidate.parent == Path(candidate.anchor):
                continue
            raise ConfigTransactionError(f"Refusing symbolic link path component: {candidate}")


def parse_toml(text: str) -> dict:
    try:
        return tomllib.loads(text)
    except Exception as exc:
        raise ConfigError(f"Codex config is not valid TOML: {exc}") from exc


def _quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def _render_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return _quote(value)
    if isinstance(value, (tuple, list)):
        return "[" + ", ".join(_render_value(item) for item in value) + "]"
    if isinstance(value, (int, float)):
        return str(value)
    raise ConfigError(f"Unsupported managed TOML value: {type(value).__name__}")


def _table_name(header: str) -> str:
    parts = []
    current = ""
    quoted = False
    for char in header.strip():
        if char == '"':
            quoted = not quoted
            continue
        if char == "." and not quoted:
            parts.append(current.strip())
            current = ""
        else:
            current += char
    parts.append(current.strip())
    return ".".join(parts)


def _table_spans(text: str):
    matches = list(_HEADER.finditer(_mask_multiline_strings(text)))
    for index, match in enumerate(matches):
        start = match.start()
        line_start = text.rfind("\n", 0, max(0, start - 1)) + 1
        preceding = text[line_start:start].rstrip("\r\n")
        if preceding.strip() == _MANAGED_MARKER:
            start = line_start
        raw_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end():raw_end]
        offset = match.end()
        last_assignment_end = match.end()
        for line in body.splitlines(keepends=True):
            offset += len(line)
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                last_assignment_end = offset
        yield _table_name(match.group(1)), start, last_assignment_end


def _mask_multiline_strings(text: str) -> str:
    """Mask TOML multiline strings while preserving offsets and newlines."""
    chars = list(text)
    index = 0
    delimiter = None
    while index < len(text):
        if delimiter is None and text.startswith('"""', index):
            delimiter = '"""'
            index += 3
            continue
        if delimiter is None and text.startswith("'''", index):
            delimiter = "'''"
            index += 3
            continue
        escaped = False
        if delimiter == '"""':
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and text[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            escaped = backslashes % 2 == 1
        if delimiter and not escaped and text.startswith(delimiter, index):
            delimiter = None
            index += 3
            continue
        if delimiter and chars[index] not in "\r\n":
            chars[index] = " "
        index += 1
    return "".join(chars)


def _block(name: str, values: dict[str, object], newline: str) -> str:
    lines = [_MANAGED_MARKER, f"[mcp_servers.{name}]"]
    lines.extend(f"{key} = {_render_value(value)}" for key, value in sorted(values.items()) if not key.startswith("expected_") and not key.startswith("functional_"))
    return newline.join(lines) + newline


def merge_managed_mcp(original: str, name: str, values: dict[str, object]) -> str:
    parsed = parse_toml(original)
    newline = "\r\n" if "\r\n" in original else "\n"
    target = f"mcp_servers.{name}"
    spans = [(start, end) for table, start, end in _table_spans(original) if table == target]
    if len(spans) > 1:
        raise ConfigCollision(f"Duplicate MCP table: {name}")
    rendered = _block(name, values, newline)
    if spans:
        start, end = spans[0]
        existing = original[start:end]
        semantic = parsed.get("mcp_servers", {}).get(name, {})
        desired = {key: value for key, value in values.items() if not key.startswith("expected_") and not key.startswith("functional_")}
        if semantic == desired and _MANAGED_MARKER in existing:
            return original
        if _MANAGED_MARKER not in existing:
            raise ConfigCollision(f"MCP name is owned by the user: {name}")
        candidate = original[:start] + rendered + original[end:]
    else:
        separator = "" if not original or original.endswith(("\n", "\r")) else newline
        if original and not original.endswith(newline * 2):
            separator += newline
        candidate = original + separator + rendered
    parse_toml(candidate)
    return candidate


def update_config_transactionally(
    path: Path,
    name: str,
    values: dict[str, object],
    validate_codex: Callable[[Path], bool],
    timestamp: str,
    events: MutableSequence[str] | None = None,
) -> TransactionResult:
    events = events if events is not None else []
    try:
        _reject_symlinked_ancestors(path)
        if path.exists() and not stat.S_ISREG(path.stat(follow_symlinks=False).st_mode):
            raise ConfigTransactionError(f"Expected regular config file: {path}")
        backup_dir = path.parent / "backups"
        _reject_symlinked_ancestors(backup_dir)
        if backup_dir.exists() and not backup_dir.is_dir():
            raise ConfigTransactionError(f"Expected backup directory: {backup_dir}")
        original = path.read_bytes() if path.exists() else b""
    except ConfigTransactionError:
        raise
    except OSError as exc:
        raise ConfigTransactionError(f"Unsafe config path: {exc}") from exc
    try:
        text = original.decode("utf-8")
        candidate_text = merge_managed_mcp(text, name, values)
    except (UnicodeError, ConfigError) as exc:
        raise ConfigTransactionError(str(exc)) from exc
    candidate = candidate_text.encode("utf-8")
    if candidate == original:
        return TransactionResult(False)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    backup = backup_dir / f"config.toml.{timestamp}"
    try:
        descriptor, temp_name = tempfile.mkstemp(prefix=".config.toml.", suffix=".tmp", dir=path.parent)
        temp_path = Path(temp_name)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(candidate)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp_path, 0o600)
        parse_toml(temp_path.read_text(encoding="utf-8"))
        events.append("candidate-validated")
        backup_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        counter = 1
        while backup.exists():
            backup = backup_dir / f"config.toml.{timestamp}.{counter}"
            counter += 1
        with backup.open("xb") as backup_handle:
            backup_handle.write(original)
        os.chmod(backup, 0o600)
        events.append("backup")
        os.replace(temp_path, path)
        temp_path = None
        events.append("replace")
        if not validate_codex(path):
            _atomic_restore(path, original)
            events.append("rollback")
            raise ConfigTransactionError("Codex rejected the updated config; original restored")
        return TransactionResult(True, str(backup))
    except ConfigTransactionError:
        raise
    except Exception as exc:
        if path.exists() and path.read_bytes() != original:
            try:
                _atomic_restore(path, original)
                events.append("rollback")
            except OSError as rollback_exc:
                raise ConfigTransactionError(f"Update failed and rollback failed: {rollback_exc}") from exc
        raise ConfigTransactionError(f"Atomic config update failed: {exc}") from exc
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def _atomic_restore(path: Path, content: bytes) -> None:
    descriptor, name = tempfile.mkstemp(prefix=".config.toml.rollback.", suffix=".tmp", dir=path.parent)
    rollback = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(rollback, 0o600)
        os.replace(rollback, path)
    finally:
        rollback.unlink(missing_ok=True)


def restore_config_exact(
    path: Path,
    content: bytes | None,
    *,
    expected_current: bytes,
    expected_inode: int,
) -> None:
    """Restore a pre-state only while the transaction still owns the file."""
    _reject_symlinked_ancestors(path)
    try:
        current_stat = path.stat(follow_symlinks=False)
    except OSError as exc:
        raise ConfigTransactionError("Config changed before rollback") from exc
    if not stat.S_ISREG(current_stat.st_mode):
        raise ConfigTransactionError(f"Expected regular config file: {path}")
    if current_stat.st_ino != expected_inode:
        raise ConfigTransactionError("Config identity changed before rollback")
    try:
        current = path.read_bytes()
    except OSError as exc:
        raise ConfigTransactionError("Config could not be verified before rollback") from exc
    if current != expected_current:
        raise ConfigTransactionError("Config content changed before rollback")
    if content is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_restore(path, content)
