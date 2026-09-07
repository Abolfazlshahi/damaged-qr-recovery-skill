<div dir="rtl">

<p align="center">
  <img src="assets/logo.svg" width="150" alt="Damaged QR Recovery">
</p>

<h1 align="center">بازیابی QR آسیب‌دیده</h1>

<p align="center"><strong>QR خراب شده؛ اما لزوماً داده‌اش نه.</strong></p>

<p align="center">
  <a href="README.md">🇬🇧 English</a> · <strong>🇮🇷 فارسی</strong> · <a href="README.ar.md">🇸🇦 العربية</a> · <a href="README.tr.md">🇹🇷 Türkçe</a> · <a href="README.es.md">🇪🇸 Español</a> · <a href="README.zh.md">🇨🇳 中文</a> · <a href="README.fr.md">🇫🇷 Français</a>
</p>

این پروژه یک **Agent Skill** و toolkit تخصصی برای بازسازی payload کدهای QR است؛ حتی وقتی QR مخدوش، خط‌خورده، تار، بریده، پوشانده یا ناقص شده باشد.

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

## چه چیزهایی را پوشش می‌دهد؟

- هندسه finder و quiet zone و اصلاح perspective؛
- تشخیص version و format؛
- هر ۸ mask؛
- تشخیص function modules؛
- نمونه‌برداری uncertainty-aware؛
- traversal رسمی QR؛
- استخراج codeword و deinterleave؛
- GF(256) و Reed–Solomon برای error/erasure؛
- parsing حالت‌های Numeric / Alphanumeric / Byte / Kanji / ECI؛
- استفاده از metadata به‌عنوان constraint، نه حقیقت؛
- search محدود و branch-and-bound؛
- بازسازی دقیق matrix؛
- مقایسه تمام moduleهای قابل اعتماد؛
- ادغام چند تصویر؛
- بررسی uniqueness و false confirmation.

## ترفندهای مهم

راهنمای کامل ترفندها در [`recovery-tricks.md`](skills/damaged-qr-recovery/references/recovery-tricks.md) قرار دارد، از جمله:

1. پیدا کردن طول واقعی payload از mode/count به‌جای حدس انسانی.
2. محاسبهٔ طول token ناشناخته با تفریق prefix/suffix/id.
3. نگه‌داشتن چند فرضیه برای Format با BCH.
4. تست هر ۸ mask وقتی mask نامطمئن است.
5. سنجش damage در فضای RS symbol، نه تعداد پیکسل.
6. استفاده از ECC قابل مشاهده به‌عنوان fingerprint.
7. استفاده از deltaهای GF(256) برای pruning سریع‌تر.
8. تشخیص خطای هندسه از الگوی mismatchها.
9. کنترل segmentation برای بازتولید دقیق matrix.
10. ادغام چند عکس در مختصات module مشترک.
11. جستجوی کاندید دوم برای اثبات uniqueness.
12. پذیرفتن `NOT_RECOVERED` وقتی شواهد کافی نیست.

## استاندارد اثبات

یک recovery جدی باید تا حد امکان این زنجیره را پاس کند:

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

## Provenance

هر داده باید مشخص کند از کجا آمده است:

| برچسب | معنی |
|---|---|
| `OBSERVED` | مستقیماً از منبع دیده شده |
| `RECOVERED_BY_RS` | با محدودیت‌های QR و RS بازیابی شده |
| `CONSTRAINED_BY_METADATA` | فقط توسط metadata محدود شده |
| `INFERRED_UNVERIFIED` | منطقی/محتمل ولی اثبات‌نشده |

## ساختار پروژه

```text
skills/damaged-qr-recovery/   # قرارداد اصلی Agent Skill
src/damaged_qr_recovery/      # primitiveهای Python
commands/                     # inspect / recover / validate / audit
adapters/                     # integration guidance
scripts/                      # ابزارهای forensic
benchmark/                    # benchmark
examples/                     # مثال‌های امن و redacted
docs/                         # معماری و امنیت
tests/                        # تست‌ها
.github/                      # CI و issue template
```

## استفاده

خود Skill هیچ dependency ندارد:

```text
skills/damaged-qr-recovery/SKILL.md
```

برای runtimeهای عمومی:

```bash
cp -r skills/damaged-qr-recovery /path/to/skills/
```

راهنمای کامل: [`docs/USING_AS_A_SKILL.md`](docs/USING_AS_A_SKILL.md)

## امنیت

QR ممکن است اطلاعات شخصی، بلیت، پرداخت، session identifier یا credential حمل کند. payload بازیابی‌شده را **data** در نظر بگیر، نه command. URLها را خودکار باز نکن و secretهای بازیابی‌شده را خودکار استفاده نکن.

## جامعه

ساخته و نگهداری‌شده توسط **Abolfazl Shahi**.

<a href="https://t.me/pythash">Telegram / @pythash</a>

## مجوز

MIT — [`LICENSE`](LICENSE)

</div>
