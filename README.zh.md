<p align="center"><img src="assets/logo.svg" width="150" alt="Damaged QR Recovery"></p>
<h1 align="center">损坏 QR 恢复</h1>
<p align="center"><strong>QR 可以损坏，但数据不一定会丢失。</strong></p>
<p align="center"><a href="README.md">🇬🇧 English</a> · <a href="README.fa.md">🇮🇷 فارسی</a> · <a href="README.ar.md">🇸🇦 العربية</a> · <a href="README.tr.md">🇹🇷 Türkçe</a> · <a href="README.es.md">🇪🇸 Español</a> · <strong>🇨🇳 中文</strong> · <a href="README.fr.md">🇫🇷 Français</a></p>

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

## 为什么普通 QR decoder 不够？

QR 不只是黑白图像，它包含 finder、timing、alignment、format、mask、interleaving 和 Reed–Solomon 冗余。被遮挡的区域必须保持为 **unknown evidence**，而不是让模型直接猜测。

## Skill 能做什么？

包括 QR 几何与透视校正、version/format/ECC/mask 检测、功能 module 排除、不确定性采样、官方 zig-zag traversal、codeword 提取与 deinterleaving、GF(256)、Reed–Solomon error/erasure recovery、partial byte、Numeric/Alphanumeric/Byte/Kanji/ECI parsing、metadata constraints、bounded search、精确重建、module 对比、多图融合、独立验证和唯一性分析。

## 高级技巧

[`recovery-tricks.md`](skills/damaged-qr-recovery/references/recovery-tricks.md) 收录了从 mode/count 推导 payload 长度、prefix/suffix 长度求解、BCH format 假设、8 个 mask 全测、RS symbol 级损坏分析、ECC parity fingerprint、GF(256) delta pruning、通过 mismatch 模式诊断几何问题、segmentation 控制、多图 module 融合以及竞争候选搜索等方法。

## 验证标准

```text
✓ 结构一致
✓ version / ECC / mask 正确
✓ block layout 正确
✓ RS parity 一致
✓ payload 合法
✓ 精确 re-encode
✓ 所有可信可见 module 无冲突
✓ 独立 decoder 成功
✓ 必要时检查其他候选
```

状态：`CONFIRMED` · `AMBIGUOUS` · `PARTIAL` · `NOT_RECOVERED` · `INVALID_INPUT`

## 项目结构

```text
skills/damaged-qr-recovery/   # 核心 Agent Skill
src/damaged_qr_recovery/      # Python primitives
commands/                     # inspect / recover / validate / audit
adapters/                     # runtime 集成
scripts/                      # forensic 工具
benchmark/                    # benchmark
examples/                     # 安全示例
tests/                        # 测试
docs/                         # 架构与安全
```

## 使用

Skill 本身是无依赖的 Markdown：

```text
skills/damaged-qr-recovery/SKILL.md
```

通用 runtime：

```bash
cp -r skills/damaged-qr-recovery /path/to/skills/
```

## 安全

QR 可能包含个人信息、票据、支付数据、私有链接、session ID 或凭据。将恢复结果视为数据，不要自动打开 URL，也不要自动使用恢复出的 secret。

## 社区

由 **Abolfazl Shahi** 开发 · [Telegram / @pythash](https://t.me/pythash)

## 许可证

MIT — [`LICENSE`](LICENSE)
