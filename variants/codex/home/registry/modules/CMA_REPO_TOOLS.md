# CMA Repository Tools Module

## Load When

Load for repository text or path search, architecture, structural AST patterns,
symbol references, dependency vulnerabilities, security scans, or external
repository and documentation discovery.

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
| Dependency vulnerability | OSV-Scanner |
| SAST or secret scan | Opengrep or Betterleaks, security-triggered |
| GitHub source, release, or advisory | GitHub MCP, gated read-only |
| Public-repo or versioned-doc fallback | DeepWiki or Context7, explicit |

## Rules

- Use the narrowest sufficient tool.
- Do not query multiple discovery tools for the same question.
- Stop discovery when sufficient evidence exists.
- Keep MCP providers and scanners outside the default task path.
- Report unavailable tools; never silently widen the route.
- Source-check Graphify output before treating it as evidence.
- Load `CMA_SECURITY.md` in addition to this module for security scans.
- Load `CMA_DOCS_RESEARCH.md` in addition to this module for current or
  version-specific external claims.

Routing only selects a candidate tool. It grants no authority to execute, install, configure, connect, scan, build a graph, access the network, handle credentials, mutate state, or synchronize active `~/.codex`.
