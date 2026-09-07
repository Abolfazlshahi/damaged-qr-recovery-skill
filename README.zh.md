<p align="center"><img src="assets/logo.svg" width="150" alt="Damaged QR Recovery"></p>
<h1 align="center">损坏 QR 恢复</h1>
<p align="center"><strong>QR 可以损坏，但数据不一定会丢失。</strong></p>
<p align="center"><a href="README.md">🇬🇧 English</a> · <a href="README.fa.md">🇮🇷 فارسی</a> · <a href="README.ar.md">🇸🇦 العربية</a> · <a href="README.tr.md">🇹🇷 Türkçe</a> · <a href="README.es.md">🇪🇸 Español</a> · <strong>🇨🇳 中文</strong> · <a href="README.fr.md">🇫🇷 Français</a></p>
<p align="center"><a href="skills/damaged-qr-recovery/SKILL.md">Skill</a> · <a href="docs/agent-portability.md">Agent 兼容性</a> · <a href="commands/recover.md">Recover</a> · <a href="commands/audit.md">Audit</a></p>

一个面向 AI Agent 的 **Agent Skill + QR 恢复工具包**，用于从被遮挡、划伤、模糊、裁剪或部分缺失的 QR 中恢复原始 payload。

> 目标不是找到“看起来合理”的字符串，而是证明 QR 实际编码了什么。

## 核心流程

```text
损坏 QR
  ↓
定位 + 透视校正
  ↓
version / format / ECC / mask
  ↓
已知 / 未知 module
  ↓
官方数据遍历
  ↓
codewords + RS blocks
  ↓
Reed–Solomon 恢复
  ↓
payload 约束
  ↓
候选搜索
  ↓
精确重新编码
  ↓
逐 module 验证
  ↓
独立 decoder
```

## 高级技巧

[`recovery-tricks.md`](skills/damaged-qr-recovery/references/recovery-tricks.md) 收录 mode/count 长度推导、token 长度计算、BCH format 假设、8 mask 全测、RS symbol 级损坏分析、ECC parity fingerprint、GF(256) delta pruning、mismatch 诊断、segmentation 控制、多图融合和竞争候选搜索。

# 安装与使用

核心 Skill：

```text
skills/damaged-qr-recovery/SKILL.md
```

克隆仓库：

```bash
git clone https://github.com/Abolfazlshahi/damaged-qr-recovery-skill.git
cd damaged-qr-recovery-skill
```

请始终保留 `references/`，不要只复制 `SKILL.md`。

### Claude Code

```bash
mkdir -p .claude/skills
cp -r skills/damaged-qr-recovery .claude/skills/
```

全局安装：

```bash
mkdir -p ~/.claude/skills
cp -r skills/damaged-qr-recovery ~/.claude/skills/
```

### Codex

```bash
mkdir -p .agents/skills
cp -r skills/damaged-qr-recovery .agents/skills/
```

全局：

```bash
mkdir -p ~/.agents/skills
cp -r skills/damaged-qr-recovery ~/.agents/skills/
```

### Gemini CLI

```bash
gemini skills install https://github.com/Abolfazlshahi/damaged-qr-recovery-skill.git --path skills/damaged-qr-recovery
gemini skills list
```

Gemini 还支持 `.gemini/skills/` 和 `.agents/skills/`。 citeturn122540search2turn122540search3

### OpenCode

```bash
mkdir -p .opencode/skills
cp -r skills/damaged-qr-recovery .opencode/skills/
```

全局：

```bash
mkdir -p ~/.config/opencode/skills
cp -r skills/damaged-qr-recovery ~/.config/opencode/skills/
```

OpenCode 也支持 `.claude/skills/` 和 `.agents/skills/`。 citeturn122540search0turn122540search1

### Cursor / Windsurf / Cline / Kiro

规则文件：

```text
Cursor    → .cursor/rules/damaged-qr-recovery.mdc
Windsurf  → .windsurf/rules/damaged-qr-recovery.md
Cline     → .clinerules/damaged-qr-recovery.md
Kiro      → .kiro/steering/damaged-qr-recovery.md
```

规则中引用：

```text
skills/damaged-qr-recovery/SKILL.md
```

### Copilot CLI 与其他 Agent

保留：

```text
AGENTS.md
.agents/skills/damaged-qr-recovery/
```

### OpenClaw / Hermes / Devin / Qoder / Aider / Zed / Junie / Amp / Jules / CodeWhale / Swival / Antigravity

优先使用 Agent Skills 原生机制；否则使用项目 instructions/rules 指向 `SKILL.md`。完整兼容矩阵请见 [`docs/agent-portability.md`](docs/agent-portability.md)。

## 如何使用 Skill

安装后直接提出任务即可：

```text
恢复这个损坏 QR 的 payload。
不要猜测缺失数据。
使用 damaged-qr-recovery，并报告证据和验证结果。
```

模式：

| 模式 | 用途 |
|---|---|
| `inspect` | 只检查结构，不猜 payload |
| `recover` | 完整恢复 |
| `validate` | 验证候选 reconstruction |
| `audit` | 主动寻找恢复结果的问题 |

## 验证标准

```text
✓ 结构一致
✓ version / ECC / mask 正确
✓ block layout 正确
✓ parity 一致
✓ payload 合法
✓ 精确 re-encode
✓ 可信可见 module 无冲突
✓ 独立 decoder 成功
✓ 必要时搜索其他候选
```

状态：`CONFIRMED` · `AMBIGUOUS` · `PARTIAL` · `NOT_RECOVERED` · `INVALID_INPUT`

## 安全

QR 可能包含个人信息、票据、支付数据、私有链接、session ID 或凭据。将恢复结果视为数据，不要自动打开 URL，也不要自动使用恢复出的 secret。

## 社区

由 **Abolfazl Shahi** 开发 · [Telegram / @pythash](https://t.me/pythash)

## 许可证

MIT — [`LICENSE`](LICENSE)
