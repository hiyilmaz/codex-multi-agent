---
name: "formproxy-security-review"
description: "Review FormProxy changes against the project's mandatory security and abuse-protection rules."
origin: "global"
---

# FormProxy Security Review

Use this skill whenever a task touches submissions, auth, plans, mail delivery, admin actions, or external integrations.

## Mandatory Checks

- Protected submissions verify Cloudflare Turnstile before processing
- Origin allowlist is enforced
- Payload validation exists at the system boundary
- Rate limits and abuse protection remain intact
- Secrets stay in environment/config, never in code
- Error responses do not leak sensitive internals

## Review Focus

- Authentication and authorization boundaries
- Tenant isolation
- Submission pipeline order
- SMTP and external provider failure handling
- Alerting and audit coverage for important failures

## Output Shape

- Findings first, ordered by severity
- Concrete file references
- Missing tests or missing verification called out explicitly
