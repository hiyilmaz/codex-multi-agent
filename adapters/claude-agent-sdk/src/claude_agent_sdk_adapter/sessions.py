from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class SessionSpec:
    session_id: str | None = None
    resume: str | None = None
    fork_session: bool = False


def _validated_id(value: str | None, field_name: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value or len(value) > 64:
        raise ValueError(f"{field_name} must be a non-empty UUID string")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError(f"{field_name} must not contain control characters")
    try:
        parsed = UUID(value)
    except (ValueError, AttributeError) as error:
        raise ValueError(f"{field_name} must be a valid UUID") from error
    if str(parsed) != value.lower():
        raise ValueError(f"{field_name} must use canonical UUID form")
    return value


def validate_session(session: SessionSpec) -> dict[str, object]:
    session_id = _validated_id(session.session_id, "session_id")
    resume = _validated_id(session.resume, "resume")
    if session_id is not None and resume is not None:
        raise ValueError("session_id and resume cannot be combined")
    if session.fork_session and resume is None:
        raise ValueError("fork_session requires resume")

    values: dict[str, object] = {}
    if session_id is not None:
        values["session_id"] = session_id
    if resume is not None:
        values["resume"] = resume
    if session.fork_session:
        values["fork_session"] = True
    return values
