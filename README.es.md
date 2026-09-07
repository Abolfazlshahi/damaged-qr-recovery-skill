<p align="center"><img src="assets/logo.svg" width="150" alt="Damaged QR Recovery"></p>
<h1 align="center">Recuperación de QR dañados</h1>
<p align="center"><strong>El QR está dañado. Los datos no tienen por qué estarlo.</strong></p>
<p align="center"><a href="README.md">🇬🇧 English</a> · <a href="README.fa.md">🇮🇷 فارسی</a> · <a href="README.ar.md">🇸🇦 العربية</a> · <a href="README.tr.md">🇹🇷 Türkçe</a> · <strong>🇪🇸 Español</strong> · <a href="README.zh.md">🇨🇳 中文</a> · <a href="README.fr.md">🇫🇷 Français</a></p>

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

## ¿Qué cubre?

Geometría de finder y quiet zone, corrección de perspectiva, versión y format, las 8 máscaras, módulos funcionales, muestreo con incertidumbre, traversal zig-zag, extracción y deinterleaving de codewords, GF(256), Reed–Solomon para errores/erasures, parsing Numeric/Alphanumeric/Byte/Kanji/ECI, restricciones de metadata, búsqueda acotada, reconstrucción exacta, comparación de módulos, fusión de varias imágenes, validación independiente y análisis de unicidad.

## Técnicas avanzadas

Consulta [`recovery-tricks.md`](skills/damaged-qr-recovery/references/recovery-tricks.md) para deducciones prácticas: longitud real desde mode/count, cálculo algebraico de tokens, hipótesis BCH para format, prueba de las 8 máscaras, análisis de daños en símbolos RS, parity fingerprints, deltas en GF(256), diagnóstico por patrones de mismatch, control de segmentation, fusión multiimagen y búsqueda de candidatos alternativos.

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

## Estructura

```text
skills/damaged-qr-recovery/   # Agent Skill principal
src/damaged_qr_recovery/      # primitives Python
commands/                     # inspect / recover / validate / audit
adapters/                     # integración con runtimes
scripts/                      # utilidades forenses
benchmark/                    # benchmarks
examples/                     # ejemplos seguros
tests/                        # pruebas
docs/                         # arquitectura y seguridad
```

## Uso

El Skill es Markdown sin dependencias:

```text
skills/damaged-qr-recovery/SKILL.md
```

Para runtimes genéricos:

```bash
cp -r skills/damaged-qr-recovery /path/to/skills/
```

## Seguridad

Un QR puede contener datos personales, tickets, pagos, enlaces privados, identificadores de sesión o credenciales. Trata el payload recuperado como datos; no abras URLs ni utilices secretos automáticamente.

## Comunidad

Desarrollado por **Abolfazl Shahi** · [Telegram / @pythash](https://t.me/pythash)

## Licencia

MIT — [`LICENSE`](LICENSE)
