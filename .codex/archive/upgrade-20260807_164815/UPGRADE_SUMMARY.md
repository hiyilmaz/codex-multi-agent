# Upgrade Summary

````text
Project upgrade target: /Users/iyilmaz/WebStorm/Codex-Multi-Agent
Variant: codex
State: managed

AGENTS.md: UNCHANGED
.codex/config.toml: UNCHANGED
.codex/prompts/fill-project-configuration.md: UPDATE
--- a/.codex/prompts/fill-project-configuration.md
+++ b/.codex/prompts/fill-project-configuration.md
@@ -43,6 +43,10 @@
 - Add `openai-docs` only for OpenAI/Codex development or documentation work
   when that skill is available in the current session. Do not add it as a
   baseline skill for unrelated projects.
+- Declare only skills that resolve from an active project, user, admin, system,
+  or session-provided surface. A skill that exists only in a disabled plugin or
+  an inactive/on-demand registry is unavailable until it is activated and
+  verified.
 - Do not remove baseline skills or agent roles that are present in
   `PROJECT_AGENTS_TEMPLATE.md` unless the user explicitly confirms removal.
 - Do not switch `ORCHESTRATION_MODE` to `skip` only because an optional skill

.codex/template-state.json: UPDATE
````
