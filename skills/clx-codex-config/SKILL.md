---
name: clx-codex-config
description: Maintain Codex global setup — AGENTS.md router, ~/.codex/rules/ (path-scoped, auto-load), ~/.codex/guides/ (on-demand), skills, plugins, hooks, and config.toml. Use when adding, editing, or wiring global guidance, rules, guides, skills, plugins, or hooks.
---

# Codex Config Maintainer

Procedural skill for changes to `$CODEX_HOME` (~/.codex). Policy gates: `~/.codex/guides/meta/meta-governance.md`, `~/.codex/guides/meta/codex-layout.md`.

CRITICAL layer distinction: `rules/*.md` WITHOUT `paths:` frontmatter are eager-loaded at session start. Only path-scoped rules belong in `rules/`; everything on-demand belongs in `guides/` (read via AGENTS.md router, never preloaded).

## Before any edit

1. Read `~/.codex/guides/meta/codex-layout.md` (structure).
2. Read `~/.codex/guides/meta/meta-governance.md` (where content belongs).
3. State intent: **add** | **edit** | **wire** | **remove**.

## Playbook A — New guide or rule

```bash
# On-demand policy → guide
# ~/.codex/guides/<meta|work>/<topic>.md   (first line after title: Load when: <triggers>)
# Wire: one row in AGENTS.md → Guide router table

# Path-scoped policy → rule (MUST have paths: frontmatter, else it eager-loads every session)
# ~/.codex/rules/<topic>.md or rules/design/<topic>.md

# Verify
rg '<topic>' ~/.codex/AGENTS.md ~/.codex/guides/ ~/.codex/rules/
```

Content: English, bullet policy, no procedural scripts (those belong in skills).

## Playbook B — New skill

```bash
# Install from GitHub
cd ~/.codex/skills/.system/skill-installer/scripts
python3 install-skill-from-github.py --repo <owner>/<repo> --path <path/in/repo> --name <skill-name>

# Or copy manually to ~/.codex/skills/<name>/SKILL.md

# Wire AGENTS.md skill router (one row)
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
codex plugin add <plugin>@claude-plugins-official   # example marketplace
# Edit ~/.codex/config.toml:
# [plugins."<plugin>@claude-plugins-official"]
# enabled = true

codex plugin list | rg '<plugin>'
```

Add AGENTS.md router row if agent must load plugin skills for a workflow.

For scaffolding new plugins, read `plugin-creator` skill.

## Playbook D — AGENTS.md change

**Allowed in AGENTS.md:** output language, precedence, always-on invariants, router tables, one-line chains, hooks reference.

**Forbidden:** multi-paragraph policy, model troubleshooting detail, design bans, git prose — those live in rules.

Template for new router row:

```markdown
| `<file-or-skill>` | <single-line load trigger> |
```

After edit, line count check: AGENTS.md should stay **under ~70 lines** unless always-on invariants grow.

## Playbook E — Hook (structural enforcement)

```bash
# 1. Write ~/.codex/hooks/<name>.py|sh (executable)
# 2. Register in ~/.codex/hooks.json PreToolUse/PostToolUse + matcher
# 3. Test:
echo '{"hook_event_name":"PreToolUse","tool_name":"..."}' | ~/.codex/hooks/<name>.py
# 4. One line in AGENTS.md § Hooks
```

## Playbook F — Remove / deprecate

1. Remove router row from AGENTS.md first (stops lazy load).
2. Delete or archive rule/skill file.
3. `config.toml`: `enabled = false` for plugins; do not leave orphan enabled entries.
4. Hooks: remove from `hooks.json` before deleting script.

## Checklist (run before finishing)

- [ ] Single source of truth — no duplicate text in AGENTS.md and rules
- [ ] Router row exists for every new rule/skill/plugin trigger
- [ ] English in meta files; user chat language unchanged (Korean)
- [ ] `meta-governance.md` / `codex-layout.md` updated if conventions changed
- [ ] User told if Codex restart needed (skills/plugins)

## Related system skills

| Skill | Use |
|-------|-----|
| `skill-creator` | Authoring new skills |
| `skill-installer` | Install from GitHub / curated lists |
| `plugin-creator` | Scaffold plugins + marketplace entries |

## Related guides

| Guide | Use |
|-------|-----|
| `~/.codex/guides/meta/codex-layout.md` | Directory tree and layer roles |
| `~/.codex/guides/meta/meta-governance.md` | Decision tree and edit discipline |
