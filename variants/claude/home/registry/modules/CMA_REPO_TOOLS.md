# CMA Repository Tools Module

## Load When

Load for repository text or path search, architecture, structural AST patterns,
symbol references, dependency vulnerabilities, security scans, external
repository and documentation discovery, or risky command isolation.

## Do Not Load When

Do not load for simple answers or tasks that already have sufficient local
evidence. Do not load multiple discovery providers for the same question.

## Tool Selection

| Need | Tool |
|---|---|
| Exact text or path | `rg` |
| Architecture or cross-file dependency | Graphify |
| Structural AST pattern | `ast-grep` |
| Symbol references or refactor radius | Serena, explicit and lazy |
| SAST or source security analysis | Opengrep, conditional |
| Dependency CVE or package vulnerability | OSV-Scanner, conditional |
| Secret exposure | Betterleaks, conditional and redacted |
| Remote repository refs, releases, PRs, issues, or advisories | GitHub, lazy and read-only |
| Public-repository conceptual knowledge | DeepWiki, lazy public-only fallback |
| Version-specific library or framework documentation | Context7, required and lazy |
| Risky or untrusted command requiring stronger isolation | cplt, only when approved and ordinary sandbox is insufficient |

## Rules

- Use local repository evidence first and stop when it is sufficient.
- Use only one external provider for one evidence need by default.
- Use the narrowest sufficient tool.
- Do not query multiple discovery tools for the same question.
- Stop discovery when sufficient evidence exists.
- Keep MCP providers and scanners outside the default task path.
- Report unavailable tools; never silently widen the route.
- Source-check Graphify output before treating it as evidence.
- Load `CMA_SECURITY.md` in addition to this module for security scans.
- Load `CMA_DOCS_RESEARCH.md` in addition to this module for current or
  version-specific external claims.
- cplt is an orthogonal execution gate, not a discovery or scanner route; load
  `CMA_SECURITY.md` and preserve every independent execution approval.

Routing only selects a candidate tool. It grants no authority to execute, install, configure, connect, scan, build a graph, access the network, handle credentials, mutate state, or synchronize active `${CLAUDE_CONFIG_DIR}`.
