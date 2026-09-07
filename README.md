<p align="center">
  <img src="assets/logo.svg" width="150" alt="Damaged QR Recovery">
</p>

<h1 align="center">Damaged QR Recovery</h1>

<p align="center"><strong>The QR is damaged. The data doesn't have to be.</strong></p>

<p align="center">
  An Agent Skill + recovery toolkit for reconstructing damaged QR payloads using QR structure, Reed–Solomon redundancy, constrained search, and exact matrix validation.
</p>

<p align="center">
  <a href="README.md"><strong>🇬🇧 English</strong></a>
  &nbsp; · &nbsp;
  <a href="README.fa.md">🇮🇷 فارسی</a>
  &nbsp; · &nbsp;
  <a href="README.ar.md">🇸🇦 العربية</a>
  &nbsp; · &nbsp;
  <a href="README.tr.md">🇹🇷 Türkçe</a>
  &nbsp; · &nbsp;
  <a href="README.es.md">🇪🇸 Español</a>
  &nbsp; · &nbsp;
  <a href="README.zh.md">🇨🇳 中文</a>
  &nbsp; · &nbsp;
  <a href="README.fr.md">🇫🇷 Français</a>
</p>

<p align="center">
  <a href="skills/damaged-qr-recovery/SKILL.md"><img src="https://img.shields.io/badge/Agent%20Skill-Damaged%20QR-2563eb?style=flat-square" alt="Agent Skill"></a>
  <a href="https://github.com/Abolfazlshahi/damaged-qr-recovery-skill/actions/workflows/test.yml"><img src="https://img.shields.io/github/actions/workflow/status/Abolfazlshahi/damaged-qr-recovery-skill/test.yml?style=flat-square&label=CI" alt="CI"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/python-3.10%2B-3776ab?style=flat-square" alt="Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-111827?style=flat-square" alt="License"></a>
</p>

<p align="center">
  <a href="skills/damaged-qr-recovery/SKILL.md">Skill</a>
  &nbsp; · &nbsp;
  <a href="docs/agent-portability.md">Agent portability</a>
  &nbsp; · &nbsp;
  <a href="commands/recover.md">Recover</a>
  &nbsp; · &nbsp;
  <a href="commands/audit.md">Audit</a>
  &nbsp; · &nbsp;
  <a href="benchmark/README.md">Benchmarks</a>
  &nbsp; · &nbsp;
  <a href="CONTRIBUTING.md">Contributing</a>
</p>

---

## The idea

```text
DAMAGED QR
    ↓
locate + rectify
    ↓
version / format / ECC / mask
    ↓
known / unknown modules
    ↓
official data traversal
    ↓
codewords + RS blocks
    ↓
Reed–Solomon recovery
    ↓
payload constraints
    ↓
exact re-encode
    ↓
visible-module proof
    ↓
independent verification
    ↓
CONFIRMED / AMBIGUOUS / NOT RECOVERED
```

> **The goal is not to find a string that works. The goal is to prove what the QR encoded.**

## What makes it different

<table>
<tr>
<td width="50%">

### Evidence-first
Unknown modules stay unknown. The system never silently turns uncertainty into a guess.

</td>
<td width="50%">

### QR-native
Recovery follows format information, masking, traversal, codewords, block structure, and ECC.

</td>
</tr>
<tr>
<td>

### Algebra before brute force
Reed–Solomon and structural constraints eliminate impossible candidates early.

</td>
<td>

### Proof, not plausibility
Candidates are re-encoded and compared against trusted visible modules.

</td>
</tr>
</table>

## Recovery ladder

| Stage | What happens |
|---|---|
| `01` | Normal decoder attempt |
| `02` | Crop / threshold / scale / perspective recovery |
| `03` | Version / format / ECC / mask analysis |
| `04` | Tri-state module matrix |
| `05` | Official QR data traversal |
| `06` | Codeword extraction + RS block reconstruction |
| `07` | Erasure/error correction |
| `08` | Payload structure and explicit constraints |
| `09` | Constrained candidate search |
| `10` | Exact re-encoding |
| `11` | Matrix-level validation |
| `12` | Independent decoding |
| `13` | Uniqueness / ambiguity analysis |

## Hard-case playbook

The advanced techniques are documented in [`recovery-tricks.md`](skills/damaged-qr-recovery/references/recovery-tricks.md):

- payload length from mode/count bits;
- algebraic token-length recovery;
- BCH format hypotheses;
- all-eight-mask testing;
- RS-symbol-level damage analysis;
- visible ECC parity fingerprints;
- GF(256) delta pruning;
- mismatch-pattern diagnosis;
- segmentation-aware exact reconstruction;
- multi-image module fusion;
- competitor search for uniqueness;
- principled `NOT_RECOVERED` outcomes.

## Confirmation standard

```text
✓ structural consistency
✓ version / ECC / mask
✓ correct RS block layout
✓ parity consistency
✓ valid payload representation
✓ exact re-encoding
✓ zero trusted visible-module contradictions
✓ independent decoder success
✓ competitor search when required
```

Final states:

`CONFIRMED` · `AMBIGUOUS` · `PARTIAL` · `NOT_RECOVERED` · `INVALID_INPUT`

## Evidence provenance

| Tag | Meaning |
|---|---|
| `OBSERVED` | Direct source evidence |
| `RECOVERED_BY_RS` | Solved from QR parity constraints |
| `CONSTRAINED_BY_METADATA` | Narrowed by trusted external context |
| `INFERRED_UNVERIFIED` | Plausible, but not proven |

External metadata can reduce the search space. It cannot replace QR evidence.

---

# Install & use

The repository is designed like a portable Agent Skill rather than a single host-specific plugin. The **canonical source of behavior is always**:

```text
skills/damaged-qr-recovery/SKILL.md
```

The skill directory should be kept intact so its `references/` files remain available through relative paths.

## Quick install — any Agent Skills compatible runtime

```bash
git clone https://github.com/Abolfazlshahi/damaged-qr-recovery-skill.git
cd damaged-qr-recovery-skill
```

Then copy or link this directory into the runtime's skill directory:

```text
skills/damaged-qr-recovery/
```

A skill-capable runtime should discover `SKILL.md` and load it when the task is about damaged QR recovery, reconstruction, validation, or auditing.

For the full runtime map, see [`docs/agent-portability.md`](docs/agent-portability.md).

## Claude Code

Claude Code uses the Agent Skills directory layout. Install the skill into your project:

```bash
mkdir -p .claude/skills
git clone https://github.com/Abolfazlshahi/damaged-qr-recovery-skill.git /tmp/damaged-qr-recovery-skill
cp -r /tmp/damaged-qr-recovery-skill/skills/damaged-qr-recovery .claude/skills/
```

Or install globally:

```bash
mkdir -p ~/.claude/skills
cp -r skills/damaged-qr-recovery ~/.claude/skills/
```

Start a new session, then ask for a damaged QR to be recovered. Claude Code can discover the `SKILL.md` and its adjacent references from the directory.

## Codex

Use the same Agent Skills layout so Codex-compatible skill discovery can find the skill:

```bash
mkdir -p .agents/skills
cp -r skills/damaged-qr-recovery .agents/skills/
```

For a user-wide installation:

```bash
mkdir -p ~/.agents/skills
cp -r skills/damaged-qr-recovery ~/.agents/skills/
```

Then start a new Codex session and ask it to inspect or recover the QR.

## OpenCode

OpenCode supports project and global Agent Skills. Put the directory here:

```bash
mkdir -p .opencode/skills
cp -r skills/damaged-qr-recovery .opencode/skills/
```

Or globally:

```bash
mkdir -p ~/.config/opencode/skills
cp -r skills/damaged-qr-recovery ~/.config/opencode/skills/
```

OpenCode also recognizes the compatibility paths `.claude/skills/` and `.agents/skills/`. citeturn122540search0turn122540search1

## Gemini CLI

Gemini CLI supports Git-based skill installation directly:

```bash
gemini skills install https://github.com/Abolfazlshahi/damaged-qr-recovery-skill.git
```

Or install only the skill directory from the repository:

```bash
gemini skills install https://github.com/Abolfazlshahi/damaged-qr-recovery-skill.git --path skills/damaged-qr-recovery
```

To check it was discovered:

```bash
gemini skills list
```

Gemini CLI also supports `~/.gemini/skills/`, `.gemini/skills/`, and the `.agents/skills/` alias. citeturn122540search2turn122540search3

## GitHub Copilot CLI

For a portable instruction-only setup, copy `AGENTS.md` into the project root:

```bash
cp AGENTS.md /path/to/your-project/AGENTS.md
```

For a repository-local skills setup on hosts that support Agent Skills, also copy:

```bash
mkdir -p /path/to/your-project/.agents/skills
cp -r skills/damaged-qr-recovery /path/to/your-project/.agents/skills/
```

Copilot CLI can also consume project instruction files. Keep the skill and the instructions separate: `SKILL.md` is the specialized recovery workflow; `AGENTS.md` is the repository-level fallback.

## Cursor

Cursor projects can keep the specialized instructions in project rules. The most portable approach is to place a small rule file that points the agent at the skill:

```text
.cursor/rules/damaged-qr-recovery.mdc
```

Recommended contents:

```text
Use the damaged-qr-recovery skill for damaged, obscured, clipped, blurred,
scratched, or partially unreadable QR recovery tasks.

Canonical skill:
skills/damaged-qr-recovery/SKILL.md
```

Keep the full skill directory in the repository or install it under `.agents/skills/` when your Cursor setup supports Agent Skills.

## Windsurf

Use a project rule under:

```text
.windsurf/rules/damaged-qr-recovery.md
```

Point it to:

```text
skills/damaged-qr-recovery/SKILL.md
```

For setups with Agent Skills support, keep the full skill under `.agents/skills/` and let the rule act as the activation hint.

## Cline

Cline can use a project rule under:

```text
.clinerules/damaged-qr-recovery.md
```

Recommended rule:

```text
For damaged QR tasks, use skills/damaged-qr-recovery/SKILL.md as the source
of truth. Preserve unknown modules, use QR structure and Reed–Solomon, and
never call a plausible payload confirmed without matrix-level validation.
```

## Kiro

Kiro can use a steering file:

```text
.kiro/steering/damaged-qr-recovery.md
```

Copy the skill directory into the project as well when Kiro is configured for Agent Skills:

```bash
mkdir -p .agents/skills
cp -r skills/damaged-qr-recovery .agents/skills/
```

## OpenClaw

OpenClaw can use the same skill directory as a custom skill. Copy it into the local skill collection:

```bash
mkdir -p ~/.openclaw/skills
a="$(pwd)/skills/damaged-qr-recovery"
cp -r "$a" ~/.openclaw/skills/
```

If your OpenClaw setup uses a skill registry, publish/import the directory there while preserving `SKILL.md` and `references/`.

## Hermes Agent

Hermes can consume the repository as an Agent Skill. Start with the canonical folder:

```text
skills/damaged-qr-recovery/
```

Use [`adapters/hermes.md`](adapters/hermes.md) for the host-specific integration notes and keep the skill directory intact.

## Devin

Use the skill as a project-level Agent Skill or custom instruction, depending on your Devin workspace configuration. The portable fallback is:

```text
skills/damaged-qr-recovery/SKILL.md
```

and repository-level guidance:

```text
AGENTS.md
```

## Grok / other plugin-capable agents

When the host supports a native skill/plugin directory, install the entire folder and preserve:

```text
SKILL.md
references/
```

When it only supports project instructions, copy `AGENTS.md` and add a short project rule pointing to the canonical `SKILL.md`.

## Aider / Zed / Junie / Amp / Jules / CodeWhale / Swival / Qoder / Antigravity

These hosts differ in how they discover persistent instructions. The portable strategy is intentionally boring:

```text
1. Keep skills/damaged-qr-recovery/ intact.
2. Copy AGENTS.md into the project when AGENTS.md is supported.
3. Add the host's small rule/instruction file pointing to SKILL.md.
4. Do not paste only a fragment of the skill; preserve references/.
```

The exact path for each host is maintained in [`docs/agent-portability.md`](docs/agent-portability.md), so the README stays readable while the compatibility matrix can evolve independently.

---

## How to use the Skill

Once installed, you do not need a special recovery prompt. Ask for the task normally:

```text
Recover the payload from this damaged QR. Do not guess missing data.
Use the damaged-qr-recovery skill and report the evidence and validation.
```

Good task inputs include:

```text
• the original QR image;
• a high-resolution crop;
• multiple photos of the same QR;
• printed metadata beside the QR;
• a known prefix/suffix/schema;
• an intact QR from the same generator.
```

The Skill should then:

```text
inspect
  → establish geometry
  → recover version/format/mask
  → build known/unknown modules
  → extract codewords
  → deinterleave RS blocks
  → solve erasures/errors
  → apply explicit constraints
  → re-encode
  → compare visible modules
  → independently decode
  → search for alternatives
```

### Explicit modes

Use the command-oriented entry points when you want a specific behavior:

| Entry point | Use it for |
|---|---|
| `inspect` | structural analysis without payload guessing |
| `recover` | full end-to-end reconstruction |
| `validate` | checking a proposed candidate |
| `audit` | actively trying to disprove a recovery |

See [`commands/`](commands/) for the exact contracts.

---

## Optional Python toolkit

```bash
python -m pip install -e '.[all]'
pytest
```

Small helper commands are available under [`scripts/`](scripts/).

```bash
python scripts/inspect_qr.py image.png
python scripts/compare_modules.py observed.png reconstructed.png --size 33
python scripts/validate_reconstruction.py reconstructed.png
```

These helpers support the methodology; they are not a claim that generic QR decoding alone can solve arbitrary damaged cases.

## Repository map

```text
.
├── skills/damaged-qr-recovery/      # canonical Agent Skill
│   ├── SKILL.md
│   └── references/                  # deep QR/RS knowledge
├── src/damaged_qr_recovery/         # Python primitives
├── commands/                        # inspect / recover / validate / audit
├── adapters/                        # runtime integration notes
├── scripts/                         # forensic helpers
├── benchmark/                       # reproducible benchmark design
├── examples/                        # safe examples
├── tests/                           # tests
├── docs/                            # architecture + portability + security
├── .github/                         # CI + issue templates
├── AGENTS.md                        # generic agent fallback
├── SECURITY.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── pyproject.toml
└── LICENSE
```

## Security

QR payloads may contain personal information, tickets, payment data, private URLs, session identifiers, or credentials. Treat recovered payloads as **data**. Do not automatically visit URLs, authenticate to services, or use recovered secrets.

For public benchmarks, use synthetic or redacted fixtures.

See [`SECURITY.md`](SECURITY.md) and [`docs/threat-model.md`](docs/threat-model.md).

## Design rule

> **Never spend certainty you do not have.**

A blurry module can remain uncertain. A partially recovered byte can remain partial. A payload can remain ambiguous.

The system becomes confident only when the evidence justifies confidence.

## Community

Built and maintained by **Abolfazl Shahi**.

<p align="center">
  <a href="https://github.com/Abolfazlshahi">GitHub</a>
  &nbsp; · &nbsp;
  <a href="https://t.me/pythash">Telegram / @pythash</a>
</p>

## License

MIT — [`LICENSE`](LICENSE).
