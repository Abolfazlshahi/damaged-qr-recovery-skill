<div dir="rtl">

<p align="center"><img src="assets/logo.svg" width="150" alt="Damaged QR Recovery"></p>
<h1 align="center">استعادة رموز QR التالفة</h1>
<p align="center"><strong>قد يتلف رمز QR، لكن بياناته لا يلزم أن تضيع.</strong></p>
<p align="center"><a href="README.md">🇬🇧 English</a> · <a href="README.fa.md">🇮🇷 فارسی</a> · <strong>🇸🇦 العربية</strong> · <a href="README.tr.md">🇹🇷 Türkçe</a> · <a href="README.es.md">🇪🇸 Español</a> · <a href="README.zh.md">🇨🇳 中文</a> · <a href="README.fr.md">🇫🇷 Français</a></p>
<p align="center"><a href="skills/damaged-qr-recovery/SKILL.md">Skill</a> · <a href="docs/agent-portability.md">دليل التوافق</a> · <a href="commands/recover.md">Recover</a> · <a href="commands/audit.md">Audit</a></p>

أداة **Agent Skill + toolkit** لإعادة بناء payload داخل رموز QR المخدوشة أو المحجوبة أو المشوشة أو المبتورة، بالاعتماد على بنية QR وتصحيح الأخطاء بدلاً من التخمين.

> الهدف ليس إيجاد نص يبدو صحيحاً؛ الهدف إثبات ما كان الرمز يشفّره فعلاً.

## الفكرة

```text
QR تالف
  ↓
هندسة + تصحيح المنظور
  ↓
Version / Format / ECC / Mask
  ↓
وحدات معروفة / مجهولة
  ↓
مسار QR الرسمي
  ↓
Codewords + RS Blocks
  ↓
Reed–Solomon
  ↓
قيود payload
  ↓
بحث المرشحين
  ↓
إعادة الترميز الدقيقة
  ↓
مقارنة كل وحدة
  ↓
تحقق مستقل
```

## لماذا لا يكفي قارئ QR عادي؟

QR ليس مجرد صورة؛ بل يحتوي على finder/timing/alignment، ومعلومات format، وmask، وinterleaving وReed–Solomon. المنطقة المحجوبة تُعامل كـ **unknown evidence** وليست مساحة للتخمين.

## التقنيات المتقدمة

[`recovery-tricks.md`](skills/damaged-qr-recovery/references/recovery-tricks.md) يغطي استنتاج طول payload من mode/count، حساب أطوال token جبرياً، فرضيات Format عبر BCH، اختبار الأقنعة الثمانية، تحليل التلف على مستوى RS symbols، parity fingerprints، delta في GF(256)، تشخيص geometry من أنماط mismatch، التحكم في segmentation، دمج الصور، والبحث عن مرشحين منافسين.

# التثبيت والاستخدام

المصدر الأساسي هو:

```text
skills/damaged-qr-recovery/SKILL.md
```

أولاً:

```bash
git clone https://github.com/Abolfazlshahi/damaged-qr-recovery-skill.git
cd damaged-qr-recovery-skill
```

احتفظ دائماً بالمجلد الكامل، بما فيه `references/`.

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

يدعم Gemini أيضاً `.gemini/skills/` و`.agents/skills/`. citeturn122540search2turn122540search3

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

كما يتعرف OpenCode على `.claude/skills/` و`.agents/skills/`. citeturn122540search0turn122540search1

### Cursor / Windsurf / Cline / Kiro

استخدم ملف القواعد الخاص بالمنصة:

```text
Cursor    → .cursor/rules/damaged-qr-recovery.mdc
Windsurf  → .windsurf/rules/damaged-qr-recovery.md
Cline     → .clinerules/damaged-qr-recovery.md
Kiro      → .kiro/steering/damaged-qr-recovery.md
```

واجعل القاعدة تشير إلى:

```text
skills/damaged-qr-recovery/SKILL.md
```

### Copilot CLI وبقية المنصات

استخدم `AGENTS.md` كطبقة fallback، واحتفظ بالمجلد الكامل للـSkill:

```text
AGENTS.md
.agents/skills/damaged-qr-recovery/
```

### OpenClaw / Hermes / Devin / Qoder / Aider / Zed / Junie / Amp / Jules / CodeWhale / Swival / Antigravity

الاستراتيجية المحمولة نفسها: native skill إن كان مدعوماً، وإلا استخدم تعليمات المشروع التي تشير إلى `SKILL.md`، مع إبقاء `references/`.

التفاصيل الدقيقة لجميع المضيفين: [`docs/agent-portability.md`](docs/agent-portability.md).

## الاستخدام

بعد التثبيت اطلب المهمة بشكل طبيعي، مثلاً:

```text
استعد payload من هذا QR التالف.
لا تخمّن البيانات المفقودة.
استخدم damaged-qr-recovery وأظهر الأدلة ونتيجة التحقق.
```

أوضاع العمل:

| الوضع | الاستخدام |
|---|---|
| `inspect` | تحليل البنية بلا تخمين |
| `recover` | الاستعادة الكاملة |
| `validate` | التحقق من مرشح موجود |
| `audit` | محاولة دحض عملية استعادة |

## معيار الإثبات

```text
✓ بنية صحيحة
✓ version / ECC / mask
✓ block layout صحيح
✓ parity متسق
✓ payload صالح
✓ إعادة ترميز دقيقة
✓ لا تناقضات في الوحدات المرئية الموثوقة
✓ decoder مستقل
✓ البحث عن بدائل عند الحاجة
```

الحالات: `CONFIRMED` · `AMBIGUOUS` · `PARTIAL` · `NOT_RECOVERED` · `INVALID_INPUT`

## الأمان

قد تحتوي رموز QR على بيانات شخصية أو تذاكر أو مدفوعات أو روابط خاصة أو session IDs أو credentials. تعامل مع payload المستعاد كبيانات، ولا تفتح الروابط أو تستخدم الأسرار تلقائياً.

## المجتمع

بواسطة **Abolfazl Shahi** · [Telegram / @pythash](https://t.me/pythash)

## الترخيص

MIT — [`LICENSE`](LICENSE)

</div>
