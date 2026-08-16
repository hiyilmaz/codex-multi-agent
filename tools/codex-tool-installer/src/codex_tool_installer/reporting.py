from __future__ import annotations

import json
from dataclasses import asdict

from .models import DiscoveryResult, RunSummary, Status


def discovery_payload(result: DiscoveryResult, selected=None, actions=None):
    selected = set(result.tools) if selected is None else set(selected)
    return {
        "platform": {
            "system": result.platform.system,
            "release": result.platform.release,
            "architecture": result.platform.machine,
            "supported": result.platform.supported,
        },
        "codex": {"installed": result.codex_installed, "config": result.config_path, "config_valid": result.config_valid},
        "tools": [
            {"name": name, "status": health.status.value, "detail": health.detail, "selected": name in selected}
            for name, health in result.tools.items()
        ],
        "selected_count": len(selected),
        "credentials": {name: {"available": available} for name, available in result.credentials.items()},
        "issues": list(result.issues),
        "planned_actions": list(actions or ()),
    }


def render_json(payload) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


def render_summary(payload) -> str:
    platform = payload["platform"]
    lines = ["Codex Development Tools Setup", "", f"Platform: {platform['system']} / {platform['architecture']}", "", "Tools:"]
    for tool in payload["tools"]:
        mark = "x" if tool["selected"] else " "
        lines.append(f"[{mark}] {tool['name']:<14} {tool['status']}")
    lines.append(f"\n{payload['selected_count']} tools selected")
    if payload.get("planned_actions"):
        lines.append("\nPlanned actions:")
        lines.extend(f"  - {action}" for action in payload["planned_actions"])
    if payload.get("credentials"):
        lines.append("\nCredentials:")
        lines.extend(f"  {name}: {'AVAILABLE' if data['available'] else 'UNAVAILABLE'}" for name, data in payload["credentials"].items())
    if payload.get("summary"):
        summary = payload["summary"]
        lines.append(f"\nCodex config: {'VALID' if summary['config_valid'] else 'INVALID'}; existing settings {'preserved' if summary['config_preserved'] else 'changed'}")
        lines.append(f"Installed: {summary['installed']} · Repaired: {summary['repaired']} · Already healthy: {summary['already_healthy']} · Failed: {summary['failed']}")
    if payload.get("issues"):
        lines.append("\nIssues:")
        lines.extend(f"  - {issue}" for issue in payload["issues"])
    return "\n".join(lines)


def summarize(final: DiscoveryResult, before: DiscoveryResult) -> RunSummary:
    installed = repaired = healthy = failed = 0
    for name, state in final.tools.items():
        old = before.tools.get(name)
        if state.status != Status.HEALTHY:
            failed += 1
        elif old and old.status == Status.MISSING:
            installed += 1
        elif old and old.status != Status.HEALTHY:
            repaired += 1
        else:
            healthy += 1
    return RunSummary(final.tools, installed, repaired, healthy, failed, final.config_valid, final.config_valid, final.credentials, final.issues)
