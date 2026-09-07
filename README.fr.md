<p align="center"><img src="assets/logo.svg" width="150" alt="Damaged QR Recovery"></p>
<h1 align="center">Récupération de QR endommagés</h1>
<p align="center"><strong>Le QR est endommagé. Les données ne sont pas forcément perdues.</strong></p>
<p align="center"><a href="README.md">🇬🇧 English</a> · <a href="README.fa.md">🇮🇷 فارسی</a> · <a href="README.ar.md">🇸🇦 العربية</a> · <a href="README.tr.md">🇹🇷 Türkçe</a> · <a href="README.es.md">🇪🇸 Español</a> · <a href="README.zh.md">🇨🇳 中文</a> · <strong>🇫🇷 Français</strong></p>
<p align="center"><a href="skills/damaged-qr-recovery/SKILL.md">Skill</a> · <a href="docs/agent-portability.md">Compatibilité agents</a> · <a href="commands/recover.md">Recover</a> · <a href="commands/audit.md">Audit</a></p>

Un **Agent Skill + toolkit** pour reconstruire le payload de QR endommagés, masqués, rayés, flous, rognés ou incomplets en exploitant leur structure et leur redondance de correction d'erreurs.

> L'objectif n'est pas de produire une chaîne plausible, mais de démontrer ce que le QR encodait réellement.

## Approche

```text
QR ENDOMMAGÉ
   ↓
géométrie + perspective
   ↓
version / format / ECC / mask
   ↓
modules connus / inconnus
   ↓
parcours officiel des données
   ↓
codewords + blocs RS
   ↓
Reed–Solomon
   ↓
contraintes du payload
   ↓
recherche de candidats
   ↓
ré-encodage exact
   ↓
comparaison module par module
   ↓
vérification indépendante
```

## Techniques avancées

[`recovery-tricks.md`](skills/damaged-qr-recovery/references/recovery-tricks.md) couvre la longueur réelle via mode/count, le calcul algébrique des tokens, les hypothèses BCH, les 8 masks, l'analyse des dommages au niveau RS, les fingerprints de parité, les deltas GF(256), le diagnostic des mismatchs, le contrôle de segmentation, la fusion multi-image et la recherche de candidats concurrents.

# Installation et utilisation

La source canonique est :

```text
skills/damaged-qr-recovery/SKILL.md
```

Clonez le dépôt :

```bash
git clone https://github.com/Abolfazlshahi/damaged-qr-recovery-skill.git
cd damaged-qr-recovery-skill
```

Conservez toujours `references/` avec le Skill.

### Claude Code

```bash
mkdir -p .claude/skills
cp -r skills/damaged-qr-recovery .claude/skills/
```

Global :

```bash
mkdir -p ~/.claude/skills
cp -r skills/damaged-qr-recovery ~/.claude/skills/
```

### Codex

```bash
mkdir -p .agents/skills
cp -r skills/damaged-qr-recovery .agents/skills/
```

Global :

```bash
mkdir -p ~/.agents/skills
cp -r skills/damaged-qr-recovery ~/.agents/skills/
```

### Gemini CLI

```bash
gemini skills install https://github.com/Abolfazlshahi/damaged-qr-recovery-skill.git --path skills/damaged-qr-recovery
gemini skills list
```

Gemini prend également en charge `.gemini/skills/` et `.agents/skills/`. citeturn122540search2turn122540search3

### OpenCode

```bash
mkdir -p .opencode/skills
cp -r skills/damaged-qr-recovery .opencode/skills/
```

Global :

```bash
mkdir -p ~/.config/opencode/skills
cp -r skills/damaged-qr-recovery ~/.config/opencode/skills/
```

OpenCode reconnaît aussi `.claude/skills/` et `.agents/skills/`. citeturn122540search0turn122540search1

### Cursor / Windsurf / Cline / Kiro

Chemins des règles :

```text
Cursor    → .cursor/rules/damaged-qr-recovery.mdc
Windsurf  → .windsurf/rules/damaged-qr-recovery.md
Cline     → .clinerules/damaged-qr-recovery.md
Kiro      → .kiro/steering/damaged-qr-recovery.md
```

Chaque règle doit pointer vers :

```text
skills/damaged-qr-recovery/SKILL.md
```

### Copilot CLI et autres agents

Conservez :

```text
AGENTS.md
.agents/skills/damaged-qr-recovery/
```

### OpenClaw / Hermes / Devin / Qoder / Aider / Zed / Junie / Amp / Jules / CodeWhale / Swival / Antigravity

Utilisez le mécanisme Agent Skills natif lorsqu'il existe. Sinon, utilisez les instructions/règles du projet qui pointent vers `SKILL.md`. Gardez toujours `references/`.

Voir la matrice complète : [`docs/agent-portability.md`](docs/agent-portability.md).

## Comment utiliser le Skill

Après installation, une demande normale suffit :

```text
Récupère le payload de ce QR endommagé.
Ne devine pas les données manquantes.
Utilise damaged-qr-recovery et montre les preuves et la validation.
```

Modes :

| Mode | Utilisation |
|---|---|
| `inspect` | Inspection structurelle sans supposition |
| `recover` | Récupération complète |
| `validate` | Validation d'un candidat |
| `audit` | Tentative de réfutation d'une récupération |

## Standard de preuve

```text
✓ structure cohérente
✓ version / ECC / mask corrects
✓ block layout correct
✓ parity cohérente
✓ payload valide
✓ ré-encodage exact
✓ aucune contradiction sur les modules visibles fiables
✓ decoder indépendant réussi
✓ recherche d'alternatives si nécessaire
```

États : `CONFIRMED` · `AMBIGUOUS` · `PARTIAL` · `NOT_RECOVERED` · `INVALID_INPUT`

## Structure

```text
skills/damaged-qr-recovery/   # Agent Skill principal
src/damaged_qr_recovery/      # primitives Python
commands/                     # inspect / recover / validate / audit
adapters/                     # intégration runtime
scripts/                      # outils forensic
benchmark/                    # benchmarks
docs/                         # architecture + sécurité + portability
tests/                        # tests
```

## Sécurité

Un QR peut contenir des données personnelles, des tickets, des paiements, des liens privés, des identifiants de session ou des credentials. Traitez le payload récupéré comme des données ; n'ouvrez pas automatiquement les URL et n'utilisez pas automatiquement les secrets récupérés.

## Communauté

Développé par **Abolfazl Shahi** · [Telegram / @pythash](https://t.me/pythash)

## Licence

MIT — [`LICENSE`](LICENSE)
