from claude_agent_sdk import ClaudeAgentOptions

from .sessions import validate_session

DISALLOWED_BUILTIN_TOOLS = (
    "AskUserQuestion",
    "Bash",
    "Edit",
    "Glob",
    "Grep",
    "KillShell",
    "NotebookEdit",
    "Read",
    "Skill",
    "Task",
    "TaskOutput",
    "TodoWrite",
    "WebFetch",
    "WebSearch",
    "Write",
)


def build_options(request):
    return ClaudeAgentOptions(
        tools=[],
        allowed_tools=[],
        setting_sources=[],
        permission_mode="dontAsk",
        disallowed_tools=list(DISALLOWED_BUILTIN_TOOLS),
        strict_mcp_config=True,
        mcp_servers={},
        max_turns=request.max_turns,
        max_budget_usd=request.max_budget_usd,
        **validate_session(request.session),
    )
