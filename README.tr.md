<div dir="ltr">

<p align="center"><img src="assets/logo.svg" width="150" alt="Damaged QR Recovery"></p>
<h1 align="center">Hasarlı QR Kurtarma</h1>
<p align="center"><strong>QR hasarlı olabilir. Veri olmak zorunda değil.</strong></p>
<p align="center"><a href="README.md">🇬🇧 English</a> · <a href="README.fa.md">🇮🇷 فارسی</a> · <a href="README.ar.md">🇸🇦 العربية</a> · <strong>🇹🇷 Türkçe</strong> · <a href="README.es.md">🇪🇸 Español</a> · <a href="README.zh.md">🇨🇳 中文</a> · <a href="README.fr.md">🇫🇷 Français</a></p>
<p align="center"><a href="skills/damaged-qr-recovery/SKILL.md">Skill</a> · <a href="docs/agent-portability.md">Agent uyumluluğu</a> · <a href="commands/recover.md">Recover</a> · <a href="commands/audit.md">Audit</a></p>

Hasarlı, karalanmış, kapatılmış, bulanık, kırpılmış veya eksik QR kodlarının payload verisini yeniden oluşturmak için **Agent Skill + recovery toolkit**.

> Amaç çalışan gibi görünen bir metin bulmak değil; QR'ın gerçekten ne kodladığını kanıtlamaktır.

## Yaklaşım

```text
HASARLI QR
   ↓
geometri + perspektif
   ↓
version / format / ECC / mask
   ↓
bilinen / bilinmeyen modüller
   ↓
official data traversal
   ↓
codewords + RS blocks
   ↓
Reed–Solomon recovery
   ↓
payload constraints
   ↓
aday araması
   ↓
tam yeniden kodlama
   ↓
modül bazlı doğrulama
   ↓
bağımsız decoder
```

## İleri teknikler

[`recovery-tricks.md`](skills/damaged-qr-recovery/references/recovery-tricks.md) mode/count ile gerçek payload uzunluğunu bulma, token uzunluğunu cebirsel çıkarma, BCH format hipotezleri, 8 mask testi, RS symbol seviyesinde hasar analizi, ECC parity fingerprint, GF(256) delta pruning, mismatch desenlerinden geometri teşhisi, segmentation kontrolü, çoklu görüntü birleştirme ve rakip aday aramasını kapsar.

# Kurulum ve kullanım

Ana Skill dosyası:

```text
skills/damaged-qr-recovery/SKILL.md
```

Önce repoyu al:

```bash
git clone https://github.com/Abolfazlshahi/damaged-qr-recovery-skill.git
cd damaged-qr-recovery-skill
```

`SKILL.md` ile birlikte `references/` klasörünü de koru.

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

Gemini ayrıca `.gemini/skills/` ve `.agents/skills/` yollarını destekler. citeturn122540search2turn122540search3

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

OpenCode `.claude/skills/` ve `.agents/skills/` yollarını da keşfeder. citeturn122540search0turn122540search1

### Cursor / Windsurf / Cline / Kiro

Kural dosyası yolları:

```text
Cursor    → .cursor/rules/damaged-qr-recovery.mdc
Windsurf  → .windsurf/rules/damaged-qr-recovery.md
Cline     → .clinerules/damaged-qr-recovery.md
Kiro      → .kiro/steering/damaged-qr-recovery.md
```

Bu dosyalar canonical Skill'i göstermelidir:

```text
skills/damaged-qr-recovery/SKILL.md
```

### Copilot CLI ve diğer hostlar

`AGENTS.md` dosyasını fallback olarak kullan ve Skill klasörünü projede tut:

```text
AGENTS.md
.agents/skills/damaged-qr-recovery/
```

### OpenClaw / Hermes / Devin / Qoder / Aider / Zed / Junie / Amp / Jules / CodeWhale / Swival / Antigravity

Host native Agent Skills destekliyorsa Skill klasörünü oraya kur. Sadece project instructions destekliyorsa `AGENTS.md` veya host'a özel rule dosyası ile `SKILL.md` dosyasını göster.

Tüm host'ların güncel yolları: [`docs/agent-portability.md`](docs/agent-portability.md).

## Skill nasıl kullanılır?

Kurulumdan sonra normal bir istek yeterli:

```text
Bu hasarlı QR'ın payload'ını kurtar.
Eksik veriyi tahmin etme.
damaged-qr-recovery kullan ve kanıtları ile doğrulama sonucunu raporla.
```

Çalışma modları:

| Mod | Amaç |
|---|---|
| `inspect` | Yapıyı tahmin etmeden inceleme |
| `recover` | Uçtan uca kurtarma |
| `validate` | Bir aday reconstruction'ı doğrulama |
| `audit` | Kurtarmanın yanlış olabileceğini aktif olarak arama |

## Doğrulama standardı

```text
✓ yapı tutarlı
✓ version / ECC / mask doğru
✓ doğru block layout
✓ parity tutarlı
✓ geçerli payload
✓ exact re-encode
✓ güvenilir görünür modüllerde sıfır çelişki
✓ bağımsız decoder başarılı
✓ gerektiğinde rakip aday araması
```

Son durumlar: `CONFIRMED` · `AMBIGUOUS` · `PARTIAL` · `NOT_RECOVERED` · `INVALID_INPUT`

## Repository yapısı

```text
skills/damaged-qr-recovery/   # canonical Skill
src/damaged_qr_recovery/      # Python primitives
commands/                     # inspect / recover / validate / audit
adapters/                     # agent entegrasyonu
scripts/                      # forensic araçları
benchmark/                    # benchmark
docs/                         # mimari + portability + güvenlik
tests/                        # testler
```

## Güvenlik

QR kişisel veri, bilet, ödeme bilgisi, private URL, session ID veya credential içerebilir. Kurtarılan payload'u **veri** olarak ele alın; URL'leri otomatik açmayın ve secret'ları otomatik kullanmayın.

## Topluluk

**Abolfazl Shahi** tarafından geliştirilir · [Telegram / @pythash](https://t.me/pythash)

## Lisans

MIT — [`LICENSE`](LICENSE)

</div>
