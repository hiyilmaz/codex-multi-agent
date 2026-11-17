# CMA Security Module

## Load When

Load for auth, permissions, secrets, trust boundaries, sandboxing, payments,
destructive operations, data loss, dependency risk, or security review.

## Do Not Load When

Do not load for changes with no security-relevant behavior beyond the short
security-reviewer no-impact check required by an approved chain.

## Rules

- Require explicit approval before security-sensitive or destructive changes.
- Fail closed on missing identity, authorization, validation, or evidence.
- Never expose credentials, tokens, private keys, or secret file contents.
- Verify the exact target before deletion, overwrite, migration, or privilege
  expansion.
- Review input validation, authorization, data exposure, secret handling,
  unsafe persistence, dependency risk, abuse paths, and rollback safety.
- The security-reviewer stage never disappears from an approved chain; return
  `NO_SECURITY_IMPACT` with evidence when no trust boundary changed.
