# Agent portability

`damaged-qr-recovery` is distributed as an ordinary Agent Skill directory. The canonical behavior is always:

```text
skills/damaged-qr-recovery/SKILL.md
```

Keep the sibling `references/` directory with it. Do not copy only selected paragraphs: the references contain the deeper procedures used when the main Skill escalates.

## Portability rule

There are two integration tiers:

### Native Agent Skills

The host discovers a directory containing `SKILL.md` and can load its supporting files on demand. Prefer this whenever available.

### Instruction-only fallback

The host does not have Agent Skills. Copy a small host-specific instruction/rule file that points the agent at `SKILL.md`, and keep the complete skill directory in the repository.

Instruction-only mode preserves the methodology but does not magically add host-native slash commands or plugin lifecycle hooks.

---

## Claude Code

Project:

```text
.claude/skills/damaged-qr-recovery/SKILL.md
```

Global:

```text
~/.claude/skills/damaged-qr-recovery/SKILL.md
```

Install from the repository checkout:

```bash
mkdir -p .claude/skills
cp -r skills/damaged-qr-recovery .claude/skills/
```

Keep `references/` beside `SKILL.md`.

### Claude Code Desktop

Use the same skill after the project is opened in Claude Code. The skill directory is the important artifact; there is no project-specific QR configuration to maintain.

---

## Codex

Project-compatible location:

```text
.agents/skills/damaged-qr-recovery/SKILL.md
```

Global-compatible location:

```text
~/.agents/skills/damaged-qr-recovery/SKILL.md
```

Install:

```bash
mkdir -p .agents/skills
cp -r skills/damaged-qr-recovery .agents/skills/
```

For a user-wide installation:

```bash
mkdir -p ~/.agents/skills
cp -r skills/damaged-qr-recovery ~/.agents/skills/
```

---

## OpenCode

OpenCode currently supports these Agent Skill locations:

```text
.opencode/skills/<name>/SKILL.md
~/.config/opencode/skills/<name>/SKILL.md
.claude/skills/<name>/SKILL.md
~/.claude/skills/<name>/SKILL.md
.agents/skills/<name>/SKILL.md
~/.agents/skills/<name>/SKILL.md
```

Recommended project installation:

```bash
mkdir -p .opencode/skills
cp -r skills/damaged-qr-recovery .opencode/skills/
```

OpenCode requires YAML frontmatter with at least `name` and `description`, which this Skill already provides. citeturn122540search0turn122540search1

---

## Gemini CLI

Install directly from Git:

```bash
gemini skills install https://github.com/Abolfazlshahi/damaged-qr-recovery-skill.git --path skills/damaged-qr-recovery
```

Check discovery:

```bash
gemini skills list
```

Useful local locations include:

```text
~/.gemini/skills/
.gemini/skills/
~/.agents/skills/
.agents/skills/
```

Gemini CLI supports both user and workspace scopes and can install from Git repositories. citeturn122540search2turn122540search3

---

## GitHub Copilot CLI

For a repository-local setup, preserve the skill under:

```text
.agents/skills/damaged-qr-recovery/
```

Also keep:

```text
AGENTS.md
```

as the instruction-only fallback for hosts that do not discover skills directly.

For global instruction-only use, Copilot CLI can use a global instructions file such as:

```text
~/.copilot/copilot-instructions.md
```

The exact command/plugin surface is host-version dependent; the skill directory itself is portable and does not depend on Copilot-specific commands.

---

## Cursor

Instruction-only setup:

```text
.cursor/rules/damaged-qr-recovery.mdc
```

Suggested content:

```text
For damaged, obscured, scratched, blurred, clipped, or partially unreadable
QR tasks, use the project's damaged-qr-recovery Agent Skill.

Canonical skill:
skills/damaged-qr-recovery/SKILL.md

Never treat a plausible payload as confirmed without QR-structure, parity,
and visible-module validation.
```

Keep the complete Skill in the repository. If your Cursor build exposes native Agent Skill discovery, use `.agents/skills/damaged-qr-recovery/` as the canonical installation path.

---

## Windsurf

Instruction-only setup:

```text
.windsurf/rules/damaged-qr-recovery.md
```

Use the same three-line activation rule as Cursor, pointing to:

```text
skills/damaged-qr-recovery/SKILL.md
```

---

## Cline

Instruction-only setup:

```text
.clinerules/damaged-qr-recovery.md
```

Minimal rule:

```text
Use skills/damaged-qr-recovery/SKILL.md for damaged QR recovery.
Treat covered modules as unknown, recover through QR structure and
Reed–Solomon where possible, and require reconstruction validation.
```

---

## Kiro

Instruction-only setup:

```text
.kiro/steering/damaged-qr-recovery.md
```

For Agent Skills-compatible configurations, additionally preserve:

```text
.agents/skills/damaged-qr-recovery/SKILL.md
```

---

## OpenClaw

Install the directory into the user's skill collection:

```bash
mkdir -p ~/.openclaw/skills
cp -r skills/damaged-qr-recovery ~/.openclaw/skills/
```

If a registry/marketplace is used by your OpenClaw deployment, import the complete directory rather than flattening the skill into a single prompt.

---

## Hermes Agent

Use:

```text
skills/damaged-qr-recovery/SKILL.md
```

and keep:

```text
skills/damaged-qr-recovery/references/
```

See [`adapters/hermes.md`](../adapters/hermes.md) for Hermes-specific notes.

---

## Devin

Use the project's Agent Skill/custom instructions facility and point to:

```text
skills/damaged-qr-recovery/SKILL.md
```

Keep `AGENTS.md` available as the generic fallback.

---

## Antigravity / Gemini-compatible hosts

Use the Gemini CLI/Agent Skills installation path when the host exposes Agent Skills. Otherwise use the generic `.agents/skills/` layout and an instruction file pointing to `SKILL.md`.

---

## Qoder

Use the native Skill mechanism when available. Otherwise keep:

```text
AGENTS.md
```

and a project rule under the host's rules directory referencing:

```text
skills/damaged-qr-recovery/SKILL.md
```

---

## Aider

Aider does not need a special QR plugin. Put the Skill reference in the project's instruction/conventions file and keep the actual directory in the repo:

```text
skills/damaged-qr-recovery/
```

---

## Zed

Use project rules/custom instructions and reference the canonical Skill path:

```text
skills/damaged-qr-recovery/SKILL.md
```

---

## JetBrains Junie

Use the project's guidelines/instructions mechanism and reference:

```text
skills/damaged-qr-recovery/SKILL.md
```

`AGENTS.md` can serve as a portable project-level fallback where supported.

---

## Amp (Sourcegraph)

Use `AGENTS.md` for persistent repository guidance and keep the complete Skill directory available to the agent:

```text
skills/damaged-qr-recovery/
```

---

## Jules

Use repository-level `AGENTS.md` together with the canonical Skill directory:

```text
skills/damaged-qr-recovery/
```

---

## CodeWhale

Use `AGENTS.md` or the host's project instructions to point to the canonical skill. No QR-specific dependency is required for the instruction layer.

---

## Swival

Use its skill library mechanism when available; otherwise stage the directory and retain `AGENTS.md` as fallback project guidance.

---

## Plugin-capable hosts in general

When the host has a plugin marketplace, a native skill registry, or an extension format, the important invariants are:

1. `SKILL.md` is the canonical behavior contract.
2. `name` in frontmatter matches the skill identifier where the host requires it.
3. `references/` remains next to the skill.
4. Relative paths inside the Skill are resolved from its own directory.
5. Installation never executes a recovered QR payload automatically.

Do not claim a native plugin integration merely because the host can read Markdown. Native plugin claims should only be added when this repository ships and tests the corresponding manifest/hooks.

---

## Why the project uses a fallback layer

Not every AI coding host implements Agent Skills the same way. Some understand `SKILL.md`; others use `AGENTS.md`, project rules, steering files, or plugin manifests.

The portability design therefore separates:

```text
behavior contract
       │
       └── SKILL.md + references/
                │
        ┌───────┴────────┐
        ↓                ↓
native skill host   instruction-only host
```

The recovery method remains identical in both cases.
