---
name: clx-claude-config
description: Maintain Claude Code global setup — CLAUDE.md router, ~/.claude/rules/ (path-scoped, auto-load), ~/.claude/guides/ (on-demand), skills, plugins, hooks, and settings.json. Use when adding, editing, or wiring global guidance, rules, guides, skills, plugins, or hooks.
---

# Claude Code Config Maintainer

Procedural skill for changes to `~/.claude/`. Policy gates: `~/.claude/guides/meta/meta-governance.md`, `~/.claude/guides/meta/claude-layout.md`.

CRITICAL layer distinction: `rules/*.md` WITHOUT `paths:` frontmatter are eager-loaded by the harness at every session start. Only path-scoped rules belong in `rules/`; everything on-demand belongs in `guides/` (read via CLAUDE.md router, never preloaded).

## Before any edit

1. Read `~/.claude/guides/meta/claude-layout.md` (structure).
2. Read `~/.claude/guides/meta/meta-governance.md` (where content belongs).
3. State intent: **add** | **edit** | **wire** | **remove**.

## Playbook A — New guide or rule

```bash
# On-demand policy → guide
# ~/.claude/guides/<meta|work>/<topic>.md   (first line after title: Load when: <triggers>)
# Wire: one row in CLAUDE.md → Guide router table

# Path-scoped policy → rule (MUST have paths: frontmatter, else it eager-loads every session)
# ~/.claude/rules/<topic>.md or rules/design/<topic>.md

# Verify
rg '<topic>' ~/.claude/CLAUDE.md ~/.claude/guides/ ~/.claude/rules/
```

Content: English, bullet policy, no procedural scripts (those belong in skills).

## Playbook B — New skill

```bash
# Manual: create the skill dir + SKILL.md
mkdir -p ~/.claude/skills/<name>   # then write SKILL.md (frontmatter: name, description)

# Packaged: install via marketplace, then enable in settings.json
claude plugin install <plugin>@<marketplace>   # or use /plugin

# Wire CLAUDE.md skill router (one row)
# Optional: rules/<topic>.md with Load when → points to this skill
```

Frontmatter required:

```yaml
---
name: skill-name
description: "One line: when to use (shown in skill discovery)."
---
```

If skill has `data/` or `scripts/`, verify paths after install (fix broken symlinks — config-doctor's symlink check catches these).

For authoring quality, also read `skill-creator` skill when writing from scratch.

## Playbook C — Enable plugin

```bash
claude plugin install <plugin>@<marketplace>   # writes enabledPlugins + extraKnownMarketplaces to settings.json
claude plugin list | rg '<plugin>'             # VERIFY it shows at the expected version (never trust exit code alone)
```

settings.json is JSON — plugin enablement lives in the top-level `"enabledPlugins"` object
(NOT a TOML `[plugins."…"]` table). A directory-marketplace plugin looks like:

```json
"extraKnownMarketplaces": { "<marketplace>": { "source": { "source": "directory", "path": "/abs/dir" } } },
"enabledPlugins": { "<plugin>@<marketplace>": true }
```

Add CLAUDE.md router row if agent must load plugin skills for a workflow.

For scaffolding new plugins, use the `plugin-dev` plugin (its create-plugin/validator/skill-reviewer skills), not a standalone skill.

## Playbook D — CLAUDE.md change

**Allowed in CLAUDE.md:** output language, precedence, always-on invariants, router tables, one-line chains, hooks reference.

**Forbidden:** multi-paragraph policy, model troubleshooting detail, design bans, git prose — those live in rules.

Template for new router row:

```markdown
| `<file-or-skill>` | <single-line load trigger> |
```

After edit, keep CLAUDE.md lean: always-on invariants + router tables + one-line chains only. Prose/policy detail belongs in rules or guides, not here.

## Playbook E — Hook (structural enforcement)

```bash
# 1. Write ~/.claude/hooks/<name>.py|sh (executable)
# 2. Register in ~/.claude/settings.json under "hooks" (event + matcher) — Claude Code has no hooks.json
# 3. Test:
echo '{"hook_event_name":"PreToolUse","tool_name":"..."}' | ~/.claude/hooks/<name>.py
# 4. One line in CLAUDE.md § Hooks
```

## Playbook F — Remove / deprecate

1. Remove router row from CLAUDE.md first (stops lazy load).
2. Delete or archive rule/skill file.
3. `settings.json`: `claude plugin uninstall <plugin>@<marketplace>` (or set its `enabledPlugins` value to `false`); optionally `claude plugin marketplace remove <marketplace>`. Verify with `claude plugin list`.
4. Hooks: remove from `settings.json` "hooks" before deleting the script; run `~/.claude/hooks/hooks-selftest.sh` after any hook change.

## Checklist (run before finishing)

- [ ] Single source of truth — no duplicate text in CLAUDE.md and rules
- [ ] Router row exists for every new rule/skill/plugin trigger
- [ ] English in meta files; user chat language unchanged (Korean)
- [ ] `meta-governance.md` / `claude-layout.md` updated if conventions changed
- [ ] User told if Claude Code restart needed (skills/plugins)

## Related system skills

| Skill | Use |
|-------|-----|
| `skill-creator` | Authoring new skills |
| `plugin-dev` | Scaffold plugins, agents, commands, hooks, marketplace entries |

Install existing skills/plugins via `/plugin` or `claude plugin install <plugin>@<marketplace>`.

## Related guides

| Guide | Use |
|-------|-----|
| `~/.claude/guides/meta/claude-layout.md` | Directory tree and layer roles |
| `~/.claude/guides/meta/meta-governance.md` | Decision tree and edit discipline |
