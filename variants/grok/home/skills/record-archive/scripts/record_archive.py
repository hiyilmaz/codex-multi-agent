#!/usr/bin/env python3
"""Validate and compact bounded project governance records."""

from __future__ import annotations

import argparse
import os
import re
import secrets
import stat
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Callable, Iterable


class ArchiveError(RuntimeError):
    pass


@dataclass(frozen=True)
class RecordPlan:
    name: str
    active_path: Path
    archive_path: Path
    active_text: str
    archive_text: str | None
    status: str
    active_count: int
    archive_count: int
    moved_count: int

    @property
    def requires_write(self) -> bool:
        return self.status == "ACTION_REQUIRED"


def managed_location(path: Path) -> tuple[Path, tuple[str, ...], str]:
    root = path.parent.parent
    try:
        relative = path.relative_to(root)
    except ValueError as error:
        raise ArchiveError(f"unsafe managed path: {path}") from error
    if (
        len(relative.parts) != 2
        or relative.parts[0] not in {"docs", "governance"}
        or relative.name in {"", ".", ".."}
    ):
        raise ArchiveError(f"unsafe managed path: {path}")
    return root, relative.parts[:-1], relative.name


def open_managed_parent(path: Path) -> tuple[int, str]:
    root, parent_parts, name = managed_location(path)
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    try:
        descriptor = os.open(root, directory_flags)
        for component in parent_parts:
            try:
                child = os.open(
                    component,
                    directory_flags,
                    dir_fd=descriptor,
                )
            finally:
                os.close(descriptor)
            descriptor = child
    except OSError as error:
        raise ArchiveError(f"unsafe managed path: {path}") from error
    return descriptor, name


def read_bytes(path: Path, required: bool = True) -> bytes | None:
    parent_descriptor, name = open_managed_parent(path)
    try:
        try:
            descriptor = os.open(
                name,
                os.O_RDONLY | os.O_NOFOLLOW,
                dir_fd=parent_descriptor,
            )
        except FileNotFoundError:
            if required:
                raise ArchiveError(f"missing managed file: {path}")
            return None
        except OSError as error:
            raise ArchiveError(f"unsafe managed path: {path}") from error
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            os.close(descriptor)
            raise ArchiveError(f"unsafe managed path: {path}")
        with os.fdopen(descriptor, "rb") as stream:
            return stream.read()
    finally:
        os.close(parent_descriptor)


def read_text(path: Path, required: bool = True) -> str | None:
    content = read_bytes(path, required=required)
    return content.decode("utf-8") if content is not None else None


def normalize_blocks(blocks: Iterable[str]) -> str:
    return "\n\n".join(block.strip() for block in blocks if block.strip())


def unique(values: Iterable[str], label: str) -> None:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            raise ArchiveError(f"duplicate {label}: {value}")
        seen.add(value)


def split_df_items(body: str, completed: bool) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"(?m)^- ID: (DF-\d{8}-\d{4}-\d{3})\s*$", body))
    if body.strip() and not matches:
        raise ArchiveError("UNSUPPORTED_FORMAT: invalid Deferred Findings item")
    items: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        block = body[match.start():end].strip()
        has_fixed = bool(re.search(r"(?m)^  Fixed At: ", block))
        if completed != has_fixed:
            section = "Completed" if completed else "Pending"
            raise ArchiveError(f"record is in wrong Deferred Findings section: {section}")
        items.append((match.group(1), block))
    return items


def parse_deferred(text: str, archive: bool = False) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    if not text.startswith("# Deferred Findings"):
        raise ArchiveError("UNSUPPORTED_FORMAT: Deferred Findings heading")
    pending_match = re.search(r"(?m)^## Pending\s*$", text)
    completed_match = re.search(r"(?m)^## Completed\s*$", text)
    headings = re.findall(r"(?m)^## (.+?)\s*$", text)
    allowed = {"Pending", "Completed"}
    if any(heading not in allowed for heading in headings) or completed_match is None:
        raise ArchiveError("UNSUPPORTED_FORMAT: Deferred Findings sections")
    if archive:
        if pending_match is not None:
            raise ArchiveError("archive must not contain a Pending section")
        pending_body = ""
    else:
        if pending_match is None or pending_match.start() > completed_match.start():
            raise ArchiveError("UNSUPPORTED_FORMAT: Pending must precede Completed")
        pending_body = text[pending_match.end():completed_match.start()]
    completed_body = text[completed_match.end():]
    return (
        split_df_items(pending_body, completed=False),
        split_df_items(completed_body, completed=True),
    )


def plan_deferred(root: Path) -> RecordPlan:
    active_path = root / "docs/DEFERRED_FINDINGS.md"
    archive_path = root / "docs/DEFERRED_FINDINGS_ARCHIVE.md"
    active_source = read_text(active_path)
    archive_source = read_text(archive_path, required=False)
    pending, completed = parse_deferred(active_source or "")
    archived = parse_deferred(archive_source, archive=True)[1] if archive_source else []
    unique((item[0] for item in pending + completed + archived), "Deferred Finding ID")
    if len(completed) < 10:
        return RecordPlan(
            "deferred-findings", active_path, archive_path, active_source or "",
            archive_source, "BELOW_THRESHOLD", len(completed), len(archived), 0
        )
    kept, moved = completed[:5], completed[5:]
    active = (
        "# Deferred Findings\n\n"
        "[Completed archive](DEFERRED_FINDINGS_ARCHIVE.md)\n\n"
        "## Pending\n\n"
        f"{normalize_blocks(item[1] for item in pending)}\n\n"
        "## Completed\n\n"
        f"{normalize_blocks(item[1] for item in kept)}\n"
    )
    archive = (
        "# Deferred Findings Archive\n\n"
        "[Back to active findings](DEFERRED_FINDINGS.md)\n\n"
        "## Completed\n\n"
        f"{normalize_blocks(item[1] for item in moved + archived)}\n"
    )
    return RecordPlan(
        "deferred-findings", active_path, archive_path, active, archive,
        "ACTION_REQUIRED", len(kept), len(moved) + len(archived), len(moved)
    )


TERMINAL_STATUSES = {"ACCEPTED", "REJECTED", "ROLLED_BACK"}
OPEN_STATUSES = {"PROPOSED", "TESTING", "REVISED", "NEED_MORE_DATA"}


def parse_experiments(text: str) -> list[tuple[str, str, str]]:
    if not text.startswith("# ") or "Experiment" not in text.splitlines()[0]:
        raise ArchiveError("UNSUPPORTED_FORMAT: experiments heading")
    matches = list(re.finditer(r"(?m)^## (EXP-\d{8}-\d{3})\b.*$", text))
    other_headings = [
        heading for heading in re.findall(r"(?m)^## (.+?)\s*$", text)
        if not heading.startswith("EXP-")
    ]
    if other_headings:
        raise ArchiveError("UNSUPPORTED_FORMAT: experiments section")
    entries: list[tuple[str, str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.start():end].strip()
        status_match = re.search(r"(?m)^Status: ([A-Z_]+)\s*$", block)
        if status_match is not None:
            status = status_match.group(1)
        else:
            legacy_result = re.search(
                r"(?mi)^- Result: (Accepted|Rejected|Rolled back)\b",
                block,
            )
            if legacy_result is None:
                raise ArchiveError(
                    f"missing experiment status: {match.group(1)}"
                )
            status = {
                "accepted": "ACCEPTED",
                "rejected": "REJECTED",
                "rolled back": "ROLLED_BACK",
            }[legacy_result.group(1).lower()]
        if status not in TERMINAL_STATUSES | OPEN_STATUSES:
            raise ArchiveError(f"unsupported experiment status: {status}")
        entries.append((match.group(1), status, block))
    if text.strip() and not matches:
        raise ArchiveError("UNSUPPORTED_FORMAT: no experiment records")
    return entries


ARCHIVE_PART_LINK = re.compile(
    r"- \[[^]]+\]\((EXPERIMENTS_ARCHIVE_(\d{3})\.md)\)"
)


def load_experiment_archive(
    root: Path,
    index_path: Path,
    index_source: str,
) -> tuple[list[tuple[str, str, str]], Path, str, list[tuple[str, str, str]]]:
    headings = re.findall(r"(?m)^## (.+?)\s*$", index_source)
    if "Archive Parts" not in headings:
        entries = parse_experiments(index_source)
        return entries, index_path, index_source, entries
    if headings != ["Archive Parts"]:
        raise ArchiveError("UNSUPPORTED_FORMAT: experiment archive index")

    heading = re.search(r"(?m)^## Archive Parts\s*$", index_source)
    assert heading is not None
    part_names: list[str] = []
    part_numbers: list[int] = []
    for line in index_source[heading.end():].splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        match = ARCHIVE_PART_LINK.fullmatch(stripped)
        if match is None:
            raise ArchiveError("UNSUPPORTED_FORMAT: experiment archive part")
        part_names.append(match.group(1))
        part_numbers.append(int(match.group(2)))
    if not part_names or part_numbers != list(range(1, len(part_names) + 1)):
        raise ArchiveError("UNSUPPORTED_FORMAT: experiment archive parts")
    unique(part_names, "experiment archive part")

    all_entries: list[tuple[str, str, str]] = []
    last_path = index_path
    last_source = index_source
    last_entries: list[tuple[str, str, str]] = []
    for part_name in part_names:
        part_path = index_path.parent / part_name
        part_source = read_text(part_path)
        part_entries = parse_experiments(part_source or "")
        all_entries.extend(part_entries)
        last_path = part_path
        last_source = part_source or ""
        last_entries = part_entries
    return all_entries, last_path, last_source, last_entries


def plan_experiments(root: Path) -> RecordPlan:
    active_path = root / "governance/EXPERIMENTS.md"
    archive_index_path = root / "governance/EXPERIMENTS_ARCHIVE.md"
    active_source = read_text(active_path)
    archive_source = read_text(archive_index_path, required=False)
    active_entries = parse_experiments(active_source or "")
    if archive_source:
        archived, archive_path, writable_archive_source, writable_entries = (
            load_experiment_archive(root, archive_index_path, archive_source)
        )
    else:
        archived = []
        archive_path = archive_index_path
        writable_archive_source = None
        writable_entries = []
    unique((entry[0] for entry in active_entries + archived), "experiment ID")
    terminal = [entry for entry in active_entries if entry[1] in TERMINAL_STATUSES]
    if len(terminal) < 10:
        return RecordPlan(
            "experiments", active_path, archive_path, active_source or "",
            writable_archive_source, "BELOW_THRESHOLD", len(terminal),
            len(archived), 0
        )
    newest_ids = {
        entry[0]
        for entry in sorted(terminal, key=lambda item: item[0], reverse=True)[:5]
    }
    kept = [
        entry for entry in active_entries
        if entry[1] in OPEN_STATUSES or entry[0] in newest_ids
    ]
    moved = [entry for entry in active_entries if entry not in kept]
    active = (
        "# Improvement Experiments\n\n"
        "[Terminal experiment archive](EXPERIMENTS_ARCHIVE.md)\n\n"
        f"{normalize_blocks(entry[2] for entry in kept)}\n"
    )
    archive = (
        "# Improvement Experiments Archive\n\n"
        "[Back to active experiments](EXPERIMENTS.md)\n\n"
        f"{normalize_blocks(entry[2] for entry in moved + writable_entries)}\n"
    )
    return RecordPlan(
        "experiments", active_path, archive_path, active, archive,
        "ACTION_REQUIRED",
        sum(entry[1] in TERMINAL_STATUSES for entry in kept),
        len(moved) + len(archived), len(moved)
    )


DATE_HEADING = re.compile(r"(?m)^## (\d{4}-\d{2}-\d{2})\s*$")
INDEX_BLOCK = re.compile(
    r"\n## Archive Index \(Previous 30 Dates\)\n.*?(?=\n## \d{4}-\d{2}-\d{2}\s*$|\Z)",
    re.MULTILINE | re.DOTALL,
)


def parse_changelog(text: str) -> tuple[str, list[tuple[str, str]]]:
    if not text.startswith("# Changelog") and not DATE_HEADING.match(text):
        raise ArchiveError("UNSUPPORTED_FORMAT: changelog heading")
    cleaned = INDEX_BLOCK.sub("", text)
    headings = re.findall(r"(?m)^## (.+?)\s*$", cleaned)
    if any(not re.fullmatch(r"\d{4}-\d{2}-\d{2}", heading) for heading in headings):
        raise ArchiveError("UNSUPPORTED_FORMAT: changelog requires date headings")
    matches = list(DATE_HEADING.finditer(cleaned))
    if not matches:
        raise ArchiveError("UNSUPPORTED_FORMAT: changelog has no date sections")
    preamble = cleaned[:matches[0].start()].strip()
    preamble = re.sub(
        r"(?m)^\[(?:Older entries|Back to active changelog)\]\([^)]+\)\s*$",
        "",
        preamble,
    ).strip()
    sections: list[tuple[str, str]] = []
    parsed_dates: list[date] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(cleaned)
        label = match.group(1)
        try:
            parsed_dates.append(date.fromisoformat(label))
        except ValueError as error:
            raise ArchiveError(f"UNSUPPORTED_FORMAT: invalid date {label}") from error
        sections.append((label, cleaned[match.start():end].strip()))
    if parsed_dates != sorted(parsed_dates, reverse=True):
        raise ArchiveError("UNSUPPORTED_FORMAT: changelog dates must be newest first")
    unique((section[0] for section in sections), "changelog date")
    return preamble, sections


def plan_changelog(root: Path) -> RecordPlan:
    active_path = root / "docs/CHANGELOG.md"
    archive_path = root / "docs/CHANGELOG_ARCHIVE.md"
    active_source = read_text(active_path)
    archive_source = read_text(archive_path, required=False)
    preamble, active_sections = parse_changelog(active_source or "")
    archived_sections = parse_changelog(archive_source)[1] if archive_source else []
    unique(
        (section[0] for section in active_sections + archived_sections),
        "changelog date",
    )
    line_count = len((active_source or "").splitlines())
    should_rotate = len(active_sections) > 20 and (
        len(active_sections) >= 30 or line_count >= 500
    )
    if not should_rotate:
        return RecordPlan(
            "changelog", active_path, archive_path, active_source or "",
            archive_source, "BELOW_THRESHOLD", len(active_sections),
            len(archived_sections), 0
        )
    kept, moved = active_sections[:20], active_sections[20:]
    merged_archive = sorted(
        moved + archived_sections,
        key=lambda section: section[0],
        reverse=True,
    )
    index = "\n".join(
        f"- [{label}](CHANGELOG_ARCHIVE.md#{label})"
        for label, _ in merged_archive[:30]
    )
    active = (
        f"{preamble or '# Changelog'}\n\n"
        "[Older entries](CHANGELOG_ARCHIVE.md)\n\n"
        "## Archive Index (Previous 30 Dates)\n\n"
        f"{index}\n\n"
        f"{normalize_blocks(section[1] for section in kept)}\n"
    )
    archive = (
        "# Changelog Archive\n\n"
        "[Back to active changelog](CHANGELOG.md)\n\n"
        f"{normalize_blocks(section[1] for section in merged_archive)}\n"
    )
    return RecordPlan(
        "changelog", active_path, archive_path, active, archive,
        "ACTION_REQUIRED", len(kept), len(merged_archive), len(moved)
    )


PLANNERS: dict[str, Callable[[Path], RecordPlan]] = {
    "deferred-findings": plan_deferred,
    "experiments": plan_experiments,
    "changelog": plan_changelog,
}


def is_dirty(root: Path, paths: Iterable[Path]) -> bool:
    probe = subprocess.run(
        ("git", "-C", str(root), "rev-parse", "--is-inside-work-tree"),
        text=True, capture_output=True, check=False,
    )
    if probe.returncode != 0:
        return False
    relative = [str(path.relative_to(root)) for path in paths]
    status = subprocess.run(
        ("git", "-C", str(root), "status", "--porcelain", "--", *relative),
        text=True, capture_output=True, check=False,
    )
    if status.returncode != 0:
        raise ArchiveError(f"git status failed: {status.stderr.strip()}")
    return bool(status.stdout.strip())


def atomic_write(path: Path, content: bytes) -> None:
    parent_descriptor, name = open_managed_parent(path)
    temporary_name = f".{name}.{os.getpid()}.{secrets.token_hex(8)}"
    descriptor: int | None = None
    try:
        try:
            metadata = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
        except FileNotFoundError:
            metadata = None
        if metadata is not None and not stat.S_ISREG(metadata.st_mode):
            raise ArchiveError(f"unsafe managed path: {path}")
        descriptor = os.open(
            temporary_name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
            dir_fd=parent_descriptor,
        )
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = None
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(
            temporary_name,
            name,
            src_dir_fd=parent_descriptor,
            dst_dir_fd=parent_descriptor,
        )
        os.fsync(parent_descriptor)
    finally:
        if descriptor is not None:
            os.close(descriptor)
        try:
            os.unlink(temporary_name, dir_fd=parent_descriptor)
        except FileNotFoundError:
            pass
        os.close(parent_descriptor)


def managed_unlink(path: Path) -> None:
    parent_descriptor, name = open_managed_parent(path)
    try:
        try:
            os.unlink(name, dir_fd=parent_descriptor)
        except FileNotFoundError:
            pass
    finally:
        os.close(parent_descriptor)


def apply_plan(plan: RecordPlan, allow_dirty: bool) -> None:
    if not plan.requires_write:
        return
    paths = (plan.active_path, plan.archive_path)
    if not allow_dirty and is_dirty(plan.active_path.parents[1], paths):
        raise ArchiveError(
            "managed files are dirty; inspect ownership and pass --allow-dirty"
        )
    originals = {
        path: read_bytes(path, required=False)
        for path in paths
    }
    replacements = {
        plan.active_path: plan.active_text.encode("utf-8"),
        plan.archive_path: (plan.archive_text or "").encode("utf-8"),
    }
    written: list[Path] = []
    try:
        for path, content in replacements.items():
            if originals[path] == content:
                continue
            written.append(path)
            atomic_write(path, content)
    except Exception:
        for path in reversed(written):
            original = originals[path]
            if original is None:
                managed_unlink(path)
            else:
                atomic_write(path, original)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "apply"))
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument(
        "--record",
        choices=(*PLANNERS, "all"),
        default="all",
    )
    parser.add_argument("--allow-dirty", action="store_true")
    arguments = parser.parse_args()
    root = arguments.root.resolve()
    selected = list(PLANNERS) if arguments.record == "all" else [arguments.record]
    plans: list[RecordPlan] = []
    for name in selected:
        active = {
            "deferred-findings": root / "docs/DEFERRED_FINDINGS.md",
            "experiments": root / "governance/EXPERIMENTS.md",
            "changelog": root / "docs/CHANGELOG.md",
        }[name]
        if arguments.record == "all" and read_bytes(active, required=False) is None:
            print(f"{name}: SKIPPED missing")
            continue
        plans.append(PLANNERS[name](root))
    if arguments.action == "apply":
        for plan in plans:
            apply_plan(plan, arguments.allow_dirty)
    for plan in plans:
        print(
            f"{plan.name}: {plan.status} active={plan.active_count} "
            f"archive={plan.archive_count} moved={plan.moved_count}"
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ArchiveError, OSError, UnicodeError) as error:
        print(f"record-archive: {error}", file=sys.stderr)
        raise SystemExit(2)
