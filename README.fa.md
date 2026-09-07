<div dir="rtl">

<p align="center">
  <img src="assets/logo.svg" width="150" alt="Damaged QR Recovery">
</p>

<h1 align="center">بازیابی QR آسیب‌دیده</h1>

<p align="center"><strong>QR خراب شده؛ اما لزوماً داده‌اش نه.</strong></p>

<p align="center">
  <a href="README.md">🇬🇧 English</a> · <strong>🇮🇷 فارسی</strong> · <a href="README.ar.md">🇸🇦 العربية</a> · <a href="README.tr.md">🇹🇷 Türkçe</a> · <a href="README.es.md">🇪🇸 Español</a> · <a href="README.zh.md">🇨🇳 中文</a> · <a href="README.fr.md">🇫🇷 Français</a>
</p>

<p align="center">
  <a href="skills/damaged-qr-recovery/SKILL.md">Skill</a> ·
  <a href="docs/agent-portability.md">سازگاری با Agentها</a> ·
  <a href="commands/recover.md">Recover</a> ·
  <a href="commands/audit.md">Audit</a>
</p>

این پروژه یک **Agent Skill + recovery toolkit** تخصصی برای بازسازی payload کدهای QR است؛ حتی وقتی QR مخدوش، خط‌خورده، تار، بریده، پوشانده یا ناقص شده باشد.

> هدف، ساختن یک رشتهٔ «محتمل» نیست؛ هدف، اثبات چیزی است که QR واقعاً encode کرده است.

## ایده

```text
QR آسیب‌دیده
    ↓
تشخیص هندسه و اصلاح پرسپکتیو
    ↓
نسخه / Format / ECC / Mask
    ↓
ماتریس known / unknown
    ↓
مسیریابی رسمی بیت‌ها
    ↓
Codeword و RS Block
    ↓
بازیابی Reed–Solomon
    ↓
محدودیت‌های payload
    ↓
جستجوی کاندیدها
    ↓
Encoding مجدد دقیق
    ↓
مقایسه module به module
    ↓
Decoder مستقل
    ↓
CONFIRMED / AMBIGUOUS / NOT_RECOVERED
```

## چرا decoder معمولی کافی نیست؟

QR فقط یک تصویر سیاه‌وسفید نیست. ساختار finder/timing/alignment، اطلاعات format، mask، interleaving و Reed–Solomon دارد. بنابراین یک ناحیه پوشانده‌شده باید به‌عنوان **unknown evidence** نگه داشته شود، نه چیزی که مدل بتواند حدس بزند.

## ترفندهای مهم

راهنمای کامل در [`recovery-tricks.md`](skills/damaged-qr-recovery/references/recovery-tricks.md) قرار دارد:

- استخراج طول واقعی payload از mode/count؛
- محاسبه طول token با prefix/suffix/id؛
- فرضیه‌های BCH برای Format؛
- تست هر ۸ mask؛
- سنجش damage در فضای RS symbol؛
- استفاده از ECC قابل مشاهده به‌عنوان fingerprint؛
- deltaهای GF(256) برای pruning؛
- تشخیص مشکل geometry از الگوی mismatch؛
- کنترل segmentation در re-encoding؛
- ادغام چند تصویر؛
- جستجوی کاندید رقیب برای uniqueness.

## استاندارد اثبات

```text
✓ ساختار معتبر
✓ version / ECC / mask صحیح
✓ block layout صحیح
✓ parity معتبر
✓ payload معتبر
✓ re-encode دقیق
✓ صفر mismatch در moduleهای معتبر
✓ decode مستقل موفق
✓ بررسی کاندیدهای رقیب
```

وضعیت نهایی:

`CONFIRMED` · `AMBIGUOUS` · `PARTIAL` · `NOT_RECOVERED` · `INVALID_INPUT`

## نصب و استفاده

خود Skill هیچ dependency ندارد و منبع اصلی آن اینجاست:

```text
skills/damaged-qr-recovery/SKILL.md
```

اول ریپو را بگیر:

```bash
git clone https://github.com/Abolfazlshahi/damaged-qr-recovery-skill.git
cd damaged-qr-recovery-skill
```

بعد پوشه Skill را در محل موردنظر Agent قرار بده:

```text
skills/damaged-qr-recovery/
```

**نکته:** فایل `references/` را حذف نکن؛ این فایل‌ها دانش عمیق موردنیاز برای caseهای سخت را نگه می‌دارند.

### Claude Code

```bash
mkdir -p .claude/skills
cp -r skills/damaged-qr-recovery .claude/skills/
```

نصب سراسری:

```bash
mkdir -p ~/.claude/skills
cp -r skills/damaged-qr-recovery ~/.claude/skills/
```

### Codex

```bash
mkdir -p .agents/skills
cp -r skills/damaged-qr-recovery .agents/skills/
```

برای نصب سراسری:

```bash
mkdir -p ~/.agents/skills
cp -r skills/damaged-qr-recovery ~/.agents/skills/
```

### Gemini CLI

نصب مستقیم از Git:

```bash
gemini skills install https://github.com/Abolfazlshahi/damaged-qr-recovery-skill.git --path skills/damaged-qr-recovery
```

بررسی:

```bash
gemini skills list
```

Gemini CLI از مسیرهای `.gemini/skills/` و `.agents/skills/` هم پشتیبانی می‌کند. citeturn122540search2turn122540search3

### OpenCode

```bash
mkdir -p .opencode/skills
cp -r skills/damaged-qr-recovery .opencode/skills/
```

نصب سراسری:

```bash
mkdir -p ~/.config/opencode/skills
cp -r skills/damaged-qr-recovery ~/.config/opencode/skills/
```

OpenCode مسیرهای `.claude/skills/` و `.agents/skills/` را هم می‌شناسد. citeturn122540search0turn122540search1

### Cursor / Windsurf / Cline / Kiro

این Agentها بسته به نسخه و تنظیمات ممکن است Skill native یا rule/instruction داشته باشند. fallback پیشنهادی:

```text
Cursor:   .cursor/rules/damaged-qr-recovery.mdc
Windsurf: .windsurf/rules/damaged-qr-recovery.md
Cline:    .clinerules/damaged-qr-recovery.md
Kiro:     .kiro/steering/damaged-qr-recovery.md
```

در فایل rule فقط به مسیر زیر اشاره کن:

```text
skills/damaged-qr-recovery/SKILL.md
```

### GitHub Copilot CLI و Agentهای مشابه

برای hostsهای instruction-based از `AGENTS.md` به‌عنوان fallback استفاده کن و پوشه Skill را هم در پروژه نگه دار:

```text
AGENTS.md
.agents/skills/damaged-qr-recovery/
```

### OpenClaw / Hermes / Devin / Qoder / Aider / Zed / Junie / Amp / Jules / CodeWhale / Swival / Antigravity

استراتژی portable یکسان است:

```text
1. پوشه skills/damaged-qr-recovery/ را کامل نگه دار.
2. اگر Agent از SKILL.md پشتیبانی می‌کند، آن را در skill directory قرار بده.
3. اگر فقط instruction می‌گیرد، AGENTS.md یا rule مخصوص همان host را اضافه کن.
4. همیشه references/ را کنار SKILL.md نگه دار.
```

راهنمای دقیق تمام مسیرها در [`docs/agent-portability.md`](docs/agent-portability.md) است.

## چطور از Skill استفاده کنیم؟

بعد از نصب، لازم نیست prompt عجیب بنویسی. کافی است درخواست معمولی بدهی:

```text
این QR آسیب‌دیده را بازیابی کن.
حدس نزن؛ از damaged-qr-recovery استفاده کن.
تمام evidence و validation را گزارش کن.
```

ورودی‌های مفید:

```text
• تصویر اصلی QR
• crop با رزولوشن بالا
• چند عکس از همان QR
• متن چاپ‌شده کنار QR
• prefix / suffix / schema معلوم
• یک QR سالم از همان generator
```

Skill باید این مسیر را دنبال کند:

```text
inspect
  → geometry
  → version / format / mask
  → known / unknown modules
  → codewords
  → RS blocks
  → erasure/error recovery
  → constraints
  → re-encode
  → visible-module validation
  → independent decode
  → uniqueness search
```

### چهار حالت کاری

| حالت | کاربرد |
|---|---|
| `inspect` | بررسی ساختار بدون حدس payload |
| `recover` | بازیابی کامل از ابتدا تا انتها |
| `validate` | بررسی یک candidate آماده |
| `audit` | تلاش فعال برای خراب‌کردن یک recovery ادعاشده |

## Provenance

| برچسب | معنی |
|---|---|
| `OBSERVED` | مستقیماً از منبع دیده شده |
| `RECOVERED_BY_RS` | با محدودیت‌های QR و RS بازیابی شده |
| `CONSTRAINED_BY_METADATA` | فقط توسط metadata محدود شده |
| `INFERRED_UNVERIFIED` | منطقی/محتمل ولی اثبات‌نشده |

## ابزار Python اختیاری

```bash
python -m pip install -e '.[all]'
pytest
```

و ابزارها:

```bash
python scripts/inspect_qr.py image.png
python scripts/compare_modules.py observed.png reconstructed.png --size 33
python scripts/validate_reconstruction.py reconstructed.png
```

## امنیت

QR ممکن است اطلاعات شخصی، بلیت، پرداخت، session identifier یا credential حمل کند. payload بازیابی‌شده را **data** در نظر بگیر، نه command. URLها را خودکار باز نکن و secretهای بازیابی‌شده را خودکار استفاده نکن.

## ساختار پروژه

```text
skills/damaged-qr-recovery/   # قرارداد اصلی Skill
src/damaged_qr_recovery/      # Python primitives
commands/                     # inspect / recover / validate / audit
adapters/                     # integration guidance
scripts/                      # ابزارهای forensic
benchmark/                    # benchmark
docs/                         # architecture / security / portability
tests/                        # tests
```

## جامعه

ساخته و نگهداری‌شده توسط **Abolfazl Shahi**.

[Telegram / @pythash](https://t.me/pythash)

## مجوز

MIT — [`LICENSE`](LICENSE)

</div>
