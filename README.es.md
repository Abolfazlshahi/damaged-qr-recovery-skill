<p align="center"><img src="assets/logo.svg" width="150" alt="Damaged QR Recovery"></p>
<h1 align="center">Recuperación de QR dañados</h1>
<p align="center"><strong>El QR está dañado. Los datos no tienen por qué estarlo.</strong></p>
<p align="center"><a href="README.md">🇬🇧 English</a> · <a href="README.fa.md">🇮🇷 فارسی</a> · <a href="README.ar.md">🇸🇦 العربية</a> · <a href="README.tr.md">🇹🇷 Türkçe</a> · <strong>🇪🇸 Español</strong> · <a href="README.zh.md">🇨🇳 中文</a> · <a href="README.fr.md">🇫🇷 Français</a></p>
<p align="center"><a href="skills/damaged-qr-recovery/SKILL.md">Skill</a> · <a href="docs/agent-portability.md">Compatibilidad con agentes</a> · <a href="commands/recover.md">Recover</a> · <a href="commands/audit.md">Audit</a></p>

**Agent Skill + toolkit** para reconstruir el payload de códigos QR dañados, ocultos, rayados, borrosos, recortados o incompletos, utilizando la estructura del propio QR y su redundancia de corrección de errores.

> El objetivo no es encontrar una cadena que “parezca correcta”, sino demostrar qué codificaba realmente el QR.

## Enfoque

```text
QR DAÑADO
   ↓
geometría + perspectiva
   ↓
version / format / ECC / mask
   ↓
módulos conocidos / desconocidos
   ↓
recorrido oficial de datos
   ↓
codewords + bloques RS
   ↓
Reed–Solomon
   ↓
restricciones del payload
   ↓
búsqueda de candidatos
   ↓
re-encoding exacto
   ↓
comparación módulo a módulo
   ↓
verificación independiente
```

## Técnicas avanzadas

[`recovery-tricks.md`](skills/damaged-qr-recovery/references/recovery-tricks.md) cubre longitud real desde mode/count, cálculo algebraico de tokens, hipótesis BCH para format, prueba de las 8 máscaras, daños a nivel de símbolos RS, parity fingerprints, deltas GF(256), diagnóstico por patrones de mismatch, control de segmentation, fusión multiimagen y búsqueda de candidatos alternativos.

# Instalación y uso

La fuente canónica es:

```text
skills/damaged-qr-recovery/SKILL.md
```

Clona el repositorio:

```bash
git clone https://github.com/Abolfazlshahi/damaged-qr-recovery-skill.git
cd damaged-qr-recovery-skill
```

Conserva siempre `SKILL.md` junto con `references/`.

### Claude Code

```bash
mkdir -p .claude/skills
cp -r skills/damaged-qr-recovery .claude/skills/
```

Global:

```bash
mkdir -p ~/.claude/skills
cp -r skills/damaged-qr-recovery ~/.claude/skills/
```

### Codex

```bash
mkdir -p .agents/skills
cp -r skills/damaged-qr-recovery .agents/skills/
```

Global:

```bash
mkdir -p ~/.agents/skills
cp -r skills/damaged-qr-recovery ~/.agents/skills/
```

### Gemini CLI

```bash
gemini skills install https://github.com/Abolfazlshahi/damaged-qr-recovery-skill.git --path skills/damaged-qr-recovery
gemini skills list
```

Gemini también descubre `.gemini/skills/` y `.agents/skills/`. citeturn122540search2turn122540search3

### OpenCode

```bash
mkdir -p .opencode/skills
cp -r skills/damaged-qr-recovery .opencode/skills/
```

Global:

```bash
mkdir -p ~/.config/opencode/skills
cp -r skills/damaged-qr-recovery ~/.config/opencode/skills/
```

OpenCode también reconoce `.claude/skills/` y `.agents/skills/`. citeturn122540search0turn122540search1

### Cursor / Windsurf / Cline / Kiro

Usa la ruta de reglas de cada host:

```text
Cursor    → .cursor/rules/damaged-qr-recovery.mdc
Windsurf  → .windsurf/rules/damaged-qr-recovery.md
Cline     → .clinerules/damaged-qr-recovery.md
Kiro      → .kiro/steering/damaged-qr-recovery.md
```

La regla debe apuntar a:

```text
skills/damaged-qr-recovery/SKILL.md
```

### Copilot CLI y otros agentes

Usa `AGENTS.md` como fallback y conserva el Skill completo:

```text
AGENTS.md
.agents/skills/damaged-qr-recovery/
```

### OpenClaw / Hermes / Devin / Qoder / Aider / Zed / Junie / Amp / Jules / CodeWhale / Swival / Antigravity

Usa la integración nativa de Skills cuando exista. En caso contrario, usa las instrucciones del proyecto para apuntar a `SKILL.md` y conserva `references/`.

La matriz completa está en [`docs/agent-portability.md`](docs/agent-portability.md).

## Cómo usar el Skill

Después de instalarlo, basta una petición normal:

```text
Recupera el payload de este QR dañado.
No adivines los datos faltantes.
Usa damaged-qr-recovery y muestra las evidencias y la validación.
```

Modos:

| Modo | Uso |
|---|---|
| `inspect` | Inspección estructural sin adivinar |
| `recover` | Recuperación completa |
| `validate` | Validar un candidato |
| `audit` | Intentar refutar una recuperación |

## Estándar de confirmación

```text
✓ estructura consistente
✓ version / ECC / mask correctos
✓ block layout correcto
✓ parity válido
✓ payload válido
✓ re-encoding exacto
✓ cero contradicciones en módulos visibles confiables
✓ decoder independiente exitoso
✓ búsqueda de alternativas cuando sea necesaria
```

Estados: `CONFIRMED` · `AMBIGUOUS` · `PARTIAL` · `NOT_RECOVERED` · `INVALID_INPUT`

## Seguridad

Un QR puede contener datos personales, tickets, pagos, enlaces privados, IDs de sesión o credenciales. Trata el payload recuperado como datos; no abras URLs ni utilices secretos automáticamente.

## Comunidad

Desarrollado por **Abolfazl Shahi** · [Telegram / @pythash](https://t.me/pythash)

## Licencia

MIT — [`LICENSE`](LICENSE)
