<div dir="rtl">

<p align="center"><img src="assets/logo.svg" width="150" alt="Damaged QR Recovery"></p>
<h1 align="center">استعادة رموز QR التالفة</h1>
<p align="center"><strong>قد يتلف رمز QR، لكن بياناته لا يلزم أن تضيع.</strong></p>
<p align="center"><a href="README.md">🇬🇧 English</a> · <a href="README.fa.md">🇮🇷 فارسی</a> · <strong>🇸🇦 العربية</strong> · <a href="README.tr.md">🇹🇷 Türkçe</a> · <a href="README.es.md">🇪🇸 Español</a> · <a href="README.zh.md">🇨🇳 中文</a> · <a href="README.fr.md">🇫🇷 Français</a></p>

أداة **Agent Skill** ومنهجية استعادة لإعادة بناء payload داخل رموز QR المخدوشة أو المحجوبة أو المشوشة أو المبتورة، بالاعتماد على بنية QR وتصحيح الأخطاء بدلاً من التخمين.

> الهدف ليس إيجاد نص يبدو صحيحاً؛ الهدف إثبات ما كان الرمز يشفّره فعلاً.

## الفكرة

```text
QR تالف
  ↓
هندسة + تصحيح المنظور
  ↓
Version / Format / ECC / Mask
  ↓
خريطة الوحدات المعروفة والمجهولة
  ↓
مسار QR الرسمي
  ↓
Codewords + RS Blocks
  ↓
Reed–Solomon
  ↓
قيود الـ payload
  ↓
بحث عن المرشحين
  ↓
إعادة ترميز دقيقة
  ↓
مقارنة كل وحدة مع المصدر
  ↓
تحقق مستقل
  ↓
CONFIRMED / AMBIGUOUS / NOT_RECOVERED
```

## لماذا لا يكفي قارئ QR عادي؟

QR نظام منظم يحتوي على finder/timing/alignment، معلومات format، masking، interleaving وReed–Solomon. المنطقة المحجوبة تُعامل كـ **معلومة مجهولة** وليست مساحة مسموحة للتخمين.

## ما الذي يغطيه الـ Skill؟

الهندسة والتصحيح، اكتشاف الإصدار وformat وECC وmask، استبعاد الوحدات الوظيفية، أخذ عينات مع الثقة، traversal الرسمي، استخراج codewords وdeinterleaving، GF(256)، تصحيح أخطاء/حذف Reed–Solomon، تحليل payload، القيود الخارجية، البحث المحدود، إعادة البناء الدقيقة، مقارنة الوحدات، دمج الصور المتعددة، التحقق المستقل وتحليل التفرد.

## التريكات المتقدمة

يركز [`recovery-tricks.md`](skills/damaged-qr-recovery/references/recovery-tricks.md) على استنتاج طول payload من mode/count، حل أطوال token جبرياً، اختبار فرضيات Format عبر BCH، اختبار الأقنعة الثمانية، قياس التلف على مستوى RS symbols، استخدام parity كـ fingerprint، delta في GF(256)، تشخيص أخطاء الهندسة من نمط الـmismatch، التحكم في segmentation، دمج الصور، والبحث عن مرشحين منافسين.

## معيار الإثبات

```text
✓ البنية صحيحة
✓ version / ECC / mask صحيحة
✓ block layout صحيح
✓ parity متسق
✓ payload صالح
✓ إعادة الترميز مطابقة
✓ لا توجد تناقضات في الوحدات المرئية الموثوقة
✓ decoder مستقل ينجح
✓ البحث عن بدائل عند الحاجة
```

الحالات النهائية: `CONFIRMED` · `AMBIGUOUS` · `PARTIAL` · `NOT_RECOVERED` · `INVALID_INPUT`

## مصدر الأدلة

| الوسم | المعنى |
|---|---|
| `OBSERVED` | ملاحظ مباشرة من المصدر |
| `RECOVERED_BY_RS` | تم استرجاعها من قيود QR/RS |
| `CONSTRAINED_BY_METADATA` | تم تضييقها بواسطة بيانات خارجية |
| `INFERRED_UNVERIFIED` | استنتاج محتمل غير مثبت |

## البنية

```text
skills/damaged-qr-recovery/   # العقد الأساسي للـ Agent
src/damaged_qr_recovery/      # أدوات Python
commands/                     # inspect / recover / validate / audit
adapters/                     # التكامل مع الـ runtimes
scripts/                      # أدوات forensic
tests/                        # الاختبارات
benchmark/                    # القياس
```

## الاستخدام

الـ Skill نفسه عبارة عن Markdown بلا dependencies:

```text
skills/damaged-qr-recovery/SKILL.md
```

للـ runtimes العامة:

```bash
cp -r skills/damaged-qr-recovery /path/to/skills/
```

## الأمان

قد تحتوي رموز QR على بيانات شخصية أو تذاكر أو معلومات دفع أو session IDs أو credentials. تعامل مع payload المستعاد كبيانات، ولا تفتح الروابط أو تستخدم الأسرار تلقائياً.

## المجتمع

بواسطة **Abolfazl Shahi** · [Telegram / @pythash](https://t.me/pythash)

## الترخيص

MIT — [`LICENSE`](LICENSE)

</div>
