<div dir="ltr">

<p align="center"><img src="assets/logo.svg" width="150" alt="Damaged QR Recovery"></p>
<h1 align="center">Hasarlı QR Kurtarma</h1>
<p align="center"><strong>QR hasarlı olabilir. Veri olmak zorunda değil.</strong></p>
<p align="center"><a href="README.md">🇬🇧 English</a> · <a href="README.fa.md">🇮🇷 فارسی</a> · <a href="README.ar.md">🇸🇦 العربية</a> · <strong>🇹🇷 Türkçe</strong> · <a href="README.es.md">🇪🇸 Español</a> · <a href="README.zh.md">🇨🇳 中文</a> · <a href="README.fr.md">🇫🇷 Français</a></p>

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

## Neden normal QR okuyucu yetmez?

QR yalnızca siyah-beyaz bir resim değildir. Finder, timing ve alignment desenleri; format bilgisi, mask, interleaving ve Reed–Solomon hata düzeltmesi içerir. Bu yüzden kapalı bir bölge doğrudan tahmin edilmez; **unknown evidence** olarak tutulur.

## Skill neleri kapsıyor?

Geometri ve perspektif düzeltme, version/format/ECC/mask keşfi, function-module ayrımı, confidence tabanlı örnekleme, resmi zig-zag traversal, codeword çıkarma, RS block deinterleaving, GF(256), Reed–Solomon error/erasure recovery, partial byte analizi, ECI ve payload parsing, metadata kısıtları, bounded search, kesin yeniden kodlama, modül karşılaştırması, çoklu görsel birleştirme, bağımsız doğrulama ve uniqueness analizi.

## İleri teknikler

[`recovery-tricks.md`](skills/damaged-qr-recovery/references/recovery-tricks.md) içinde mode/count ile gerçek payload uzunluğunu bulma, prefix/suffix uzunluk hesabı, BCH format hipotezleri, 8 mask testi, RS-symbol seviyesinde hasar analizi, görünür ECC parity fingerprint, GF(256) delta pruning, mismatch desenlerinden geometri teşhisi, segmentation kontrolü ve rakip aday araması bulunur.

## Kanıt standardı

```text
✓ doğru yapı
✓ version / ECC / mask
✓ doğru block layout
✓ geçerli RS parity
✓ geçerli payload
✓ exact re-encode
✓ görünür modüllerde sıfır çelişki
✓ bağımsız decoder başarısı
✓ gerektiğinde alternatif aday araması
```

Durumlar: `CONFIRMED` · `AMBIGUOUS` · `PARTIAL` · `NOT_RECOVERED` · `INVALID_INPUT`

## Repository

```text
skills/damaged-qr-recovery/   # ana Agent Skill
src/damaged_qr_recovery/      # Python primitives
commands/                     # inspect / recover / validate / audit
adapters/                     # runtime entegrasyonu
scripts/                      # forensic araçları
benchmark/                    # benchmark
examples/                     # güvenli örnekler
tests/                        # testler
docs/                         # mimari + güvenlik
```

## Kullanım

Skill'in kendisi bağımlılıksız Markdown'dır:

```text
skills/damaged-qr-recovery/SKILL.md
```

Genel Skill runtime'ları için:

```bash
cp -r skills/damaged-qr-recovery /path/to/skills/
```

## Güvenlik

QR kodları kişisel bilgi, bilet, ödeme verisi, session ID veya kimlik doğrulama bilgisi içerebilir. Kurtarılan payload'ları veri olarak ele alın; URL'leri otomatik açmayın ve secret'ları otomatik kullanmayın.

## Topluluk

**Abolfazl Shahi** tarafından geliştirilir · [Telegram / @pythash](https://t.me/pythash)

## Lisans

MIT — [`LICENSE`](LICENSE)

</div>
