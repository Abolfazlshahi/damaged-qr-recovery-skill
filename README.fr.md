<p align="center"><img src="assets/logo.svg" width="150" alt="Damaged QR Recovery"></p>
<h1 align="center">Récupération de QR endommagés</h1>
<p align="center"><strong>Le QR est endommagé. Les données ne sont pas forcément perdues.</strong></p>
<p align="center"><a href="README.md">🇬🇧 English</a> · <a href="README.fa.md">🇮🇷 فارسی</a> · <a href="README.ar.md">🇸🇦 العربية</a> · <a href="README.tr.md">🇹🇷 Türkçe</a> · <a href="README.es.md">🇪🇸 Español</a> · <a href="README.zh.md">🇨🇳 中文</a> · <strong>🇫🇷 Français</strong></p>

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

## Pourquoi un lecteur QR classique ne suffit pas ?

Un QR n'est pas une simple image noir et blanc. Il contient des motifs finder/timing/alignment, des informations de format, un masque, de l'interleaving et de la correction Reed–Solomon. Une zone masquée doit donc rester **inconnue**, et non devenir une supposition.

## Couverture du Skill

Géométrie et correction de perspective, détection version/format/ECC/mask, modules fonctionnels, échantillonnage avec incertitude, traversal zig-zag officiel, extraction/deinterleaving des codewords, GF(256), correction Reed–Solomon erreurs/effacements, parsing Numeric/Alphanumeric/Byte/Kanji/ECI, contraintes de metadata, recherche bornée, reconstruction exacte, comparaison des modules, fusion multi-image, validation indépendante et analyse d'unicité.

## Techniques avancées

[`recovery-tricks.md`](skills/damaged-qr-recovery/references/recovery-tricks.md) couvre notamment la longueur réelle du payload via mode/count, le calcul des longueurs de token, les hypothèses BCH pour le format, les 8 masques, l'analyse des dégâts au niveau des symboles RS, les fingerprints de parité, les deltas GF(256), le diagnostic par motifs de mismatch, le contrôle de segmentation, la fusion multi-image et la recherche de candidats concurrents.

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
examples/                     # exemples sûrs
tests/                        # tests
docs/                         # architecture et sécurité
```

## Utilisation

Le Skill lui-même est un Markdown sans dépendance :

```text
skills/damaged-qr-recovery/SKILL.md
```

Pour les runtimes génériques :

```bash
cp -r skills/damaged-qr-recovery /path/to/skills/
```

## Sécurité

Un QR peut contenir des données personnelles, tickets, paiements, liens privés, identifiants de session ou credentials. Traitez le payload récupéré comme des données ; n'ouvrez pas automatiquement les URL et n'utilisez pas automatiquement les secrets récupérés.

## Communauté

Développé par **Abolfazl Shahi** · [Telegram / @pythash](https://t.me/pythash)

## Licence

MIT — [`LICENSE`](LICENSE)
