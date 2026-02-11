# HTML Encoding Sorunu Çözümü / HTML Encoding Issue Resolution

## Problem / Issue

Pine Script editöründe şu hata alıyorsanız:
If you're getting this error in Pine Script editor:

```
Syntax error at input '=>'
```

veya kod içinde `=&gt;` görüyorsanız, bu HTML encoding sorunudur.
or you see `=&gt;` in the code, this is an HTML encoding issue.

## Durum / Status

**✅ Repository'deki tüm dosyalar DOĞRU / All files in repository are CORRECT**

```bash
$ grep -c "=&gt;" V7_5_07226.txt
0    # ← DOĞRU: Hiç HTML encoding yok / CORRECT: No HTML encoding
```

## Neden Oluyor? / Why Does This Happen?

HTML encoding **SADECE** şu durumlarda oluşur / happens **ONLY** when:

1. GitHub web sayfasından kod kopyalama / Copying code from GitHub web pages
2. PR açıklaması veya yorumlardan kopyalama / Copying from PR descriptions or comments
3. Markdown rendered view'dan kopyalama / Copying from markdown rendered views

**Kaynak dosyalarda sorun YOK!** / **Source files have NO problem!**

## Çözümler / Solutions

### Çözüm 1: Repository'den Doğrudan Al (ÖNERİLEN)

**Git clone kullan / Use git clone:**

```bash
git clone https://github.com/dmelmes/070226birlesik.git
cd 070226birlesik
git checkout copilot/add-confirmed-buy-module
```

Sonra `V7_5_07226.txt` dosyasını **doğrudan** TradingView'e yükle.

### Çözüm 2: Raw File İndir

**Wget ile:**
```bash
wget https://raw.githubusercontent.com/dmelmes/070226birlesik/copilot/add-confirmed-buy-module/V7_5_07226.txt
```

**Curl ile:**
```bash
curl -o V7_5_07226.txt https://raw.githubusercontent.com/dmelmes/070226birlesik/copilot/add-confirmed-buy-module/V7_5_07226.txt
```

### Çözüm 3: GitHub Raw Button

1. Şu linke git / Go to: https://github.com/dmelmes/070226birlesik/blob/copilot/add-confirmed-buy-module/V7_5_07226.txt
2. Sağ üstteki **"Raw"** butonuna tıkla / Click **"Raw"** button (top right)
3. Tüm metni seç / Select all: `Ctrl+A` 
4. Kopyala / Copy: `Ctrl+C`
5. TradingView'e yapıştır / Paste to TradingView: `Ctrl+V`

### Çözüm 4: Otomatik Düzeltme Script

Eğer dosyanızda `=&gt;` varsa, otomatik düzelt:
If your file has `=&gt;`, auto-fix it:

```bash
./fix_html_encoding.sh V7_5_07226.txt
```

veya manuel / or manual:

```bash
sed -i 's/=&gt;/=>/g' V7_5_07226.txt
```

## Test Et / Verify

Dosyanızı kontrol edin / Check your file:

```bash
# HTML encoding var mı? / Any HTML encoding?
grep "=&gt;" V7_5_07226.txt

# Hiçbir şey göstermemeli (0 sonuç)
# Should show nothing (0 results)
```

```bash
# Doğru operator sayısı / Count correct operators
grep -o "=>" V7_5_07226.txt | wc -l

# 76 olmalı / Should be 76
```

## Doğru Syntax / Correct Syntax

**DOĞRU ✅ / CORRECT ✅:**
```pinescript
f_alphatrend(coeff, AP, novolumedata) =>
    _ATR = ta.sma(ta.tr, AP)
    ...

f_at_add_outcome(arr, pct, lastN) =>
    array.unshift(arr, pct)
    ...
```

**YANLIŞ ❌ / WRONG ❌:**
```
f_at_add_outcome(arr, pct, lastN) =&gt;   // HTML encoded!
```

## Özet / Summary

| Durum | Status |
|-------|--------|
| Repository dosyası | ✅ DOĞRU / CORRECT |
| HTML encoding | ❌ YOK / NONE |
| Pine Script uyumluluk | ✅ UYUMLU / COMPATIBLE |
| Kullanıma hazır | ✅ EVET / YES |

**Sorun repository'de değil, kopyalama metodunda!**  
**Problem is not in repository, it's in the copy method!**

## Dosyalar / Files

- `V7_5_07226.txt` - Ana Pine Script dosyası (DOĞRU)
- `fix_html_encoding.sh` - Otomatik düzeltme script'i
- `HTML_ENCODING_FIX_README.md` - Bu dosya

## İletişim / Contact

Sorun devam ederse, lütfen:
If problem persists, please:

1. Dosyayı nasıl aldığınızı belirtin (git clone, web, vb.)
2. Hangi editörü kullandığınızı belirtin
3. Hata mesajının tam ekran görüntüsünü paylaşın

---

**Son Güncelleme / Last Updated:** 2026-02-11  
**Durum / Status:** ✅ ÇÖZÜLDÜ / RESOLVED
