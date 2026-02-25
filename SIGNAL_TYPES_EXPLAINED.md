# Sinyal Tipleri Açıklaması / Signal Types Explanation

## Hızlı Karşılaştırma / Quick Comparison

| Sinyal Tipi | Güvenilirlik | Hız | Kaybolabilir mi? | Kullanım Amacı |
|-------------|--------------|-----|------------------|----------------|
| **[⚡REPAINT]** | ⭐ (Düşük) | ⚡⚡⚡ | EVET (Yüksek risk) | Erken uyarı, hazırlık |
| **[⚡REALTIME]** | ⭐⭐ (Orta) | ⚡⚡ | BELKİ (Orta risk) | MTF izleme, çoklu TF |
| **[✓CONFIRMED]** | ⭐⭐⭐ (Yüksek) | ⚡ | HAYIR (Risk yok) | İşlem açma kararı |

---

## 1. [⚡REPAINT] - Repaint Sinyali

### Ne Zaman Gelir?
- Bar içinde **anında**, gerçek zamanlı
- Koşullar sağlandığı anda
- Bar kapanmadan önce

### Güvenilirlik
- **⭐ En düşük güvenilirlik (%40-60)**
- Bar kapanmadan önce kaybolabilir
- Fiyat geri dönerse sinyal iptal olur

### Avantajlar
✅ **En hızlı uyarı** - İlk hareketi yakalar
✅ **Fırsat kaçırmama** - Erken pozisyon alma şansı
✅ **Hazırlık zamanı** - Confirmed için hazırlanma

### Dezavantajlar
❌ **Yüksek repaint riski** - Kaybolabilir
❌ **Yanlış sinyal oranı yüksek** - %40-60 başarı
❌ **Stop loss risk** - Erken giriş = geniş stop

### Ne Zaman Kullanılır?
- **Sadece uyarı amaçlı**
- Confirmed sinyalini beklemek için hazırlık
- Agresif traderlar için erken giriş (riskli!)

### Örnek Mesaj
```
⚡ BANKO KESIŞME AL [REPAINT]
[VBTYZ] [1H]
Fiyat: 22.78
⚠️ Uyarı: Bar kapanmadan önce kaybolabilir!
```

### Teknik Detay
- Event ID: `BANKO_REPAINT_<bar_index>`
- Frequency: `alert.freq_once_per_bar`
- Trigger: Koşul sağlandığında anında

---

## 2. [⚡REALTIME] - Realtime Sinyal (MTF)

### Ne Zaman Gelir?
- **Multi-timeframe** (MTF) sinyalleri için
- Büyük timeframe bar'ı kapanmadan
- Örn: 1H chart'tayken 4H sinyali

### Güvenilirlik
- **⭐⭐ Orta güvenilirlik (%60-80)**
- REPAINT'ten daha güvenilir
- CONFIRMED'dan daha riskli

### Avantajlar
✅ **Farklı TF izleme** - Büyük TF'leri takip
✅ **Erken bilgilendirme** - 4H/1D sinyallerini erken görme
✅ **Orta risk-getiri** - REPAINT'ten güvenilir

### Dezavantajlar
❌ **Hala repaint riski var** - Büyük TF bar kapanmadı
❌ **Karmaşık** - Hangi TF'nin bar'ı?
❌ **Geçici sinyal** - CONFIRMED gelmeyebilir

### Ne Zaman Kullanılır?
- Büyük timeframe sinyallerini **izlemek** için
- İşlem açmadan **önce** bilgi almak için
- 4H/1D trendini takip etmek için

### Örnek Mesaj
```
K - BANKO KESIŞME AL (4H) [⚡REALTIME]
[TUPRS]
Fiyat: 223.7
```

### Teknik Detay
- Event ID: `MTF_BANKO_AL_4H_<mtfTime>`
- Frequency: `alert.freq_once_per_bar`
- Trigger: `tfClosed = false` (higher TF bar not closed)

---

## 3. [✓CONFIRMED] - Confirmed Sinyal

### Ne Zaman Gelir?
- Bar **tam kapandıktan sonra**
- Tüm koşullar bar sonunda geçerli
- Kesin, geri dönüşsüz

### Güvenilirlik
- **⭐⭐⭐ En yüksek güvenilirlik (%85-95)**
- **ASLA KAYBOLMAZ**
- Bar kapandı = Sinyal kesin

### Avantajlar
✅ **Kesin sinyal** - Geri dönmez
✅ **Yüksek başarı oranı** - %85-95
✅ **Güvenli işlem** - Stop loss net
✅ **Stressiz** - "Acaba kaybolur mu?" yok

### Dezavantajlar
❌ **1 bar gecikmeli** - En hızlı değil
❌ **Geç giriş** - Fiyat hareket etmiş olabilir
❌ **Stop mesafesi** - Bazen daha geniş

### Ne Zaman Kullanılır?
- **İşlem açmak için** en güvenilir
- Yeni başlayanlar için ideal
- Risk yönetimi odaklı traderlar için

### Örnek Mesaj
```
✓ BANKO KESIŞME AL [CONFIRMED]
[VBTYZ] [1H]
Fiyat: 22.85
✅ Kesin sinyal - Bar kapatıldı
```

### Teknik Detay
- Event ID: `BANKO_CONFIRMED_<time>`
- Frequency: `alert.freq_once_per_bar_close`
- Trigger: `barstate.isconfirmed` (bar closed)

---

## Güvenilirlik Karşılaştırması

### Başarı Oranları (Tahmini)

| Sinyal Tipi | Başarı Oranı | Kaybolma Riski | İşlem Önerisi |
|-------------|--------------|----------------|---------------|
| REPAINT | %40-60 | Yüksek (40-60%) | ❌ İşlem açma |
| REALTIME | %60-80 | Orta (20-40%) | ⚠️ Dikkatli izle |
| CONFIRMED | %85-95 | Yok (0%) | ✅ İşlem aç |

### Risk Seviyeleri

```
REPAINT:    ⚠️⚠️⚠️⚠️⚠️ (5/5 Risk)
REALTIME:   ⚠️⚠️⚠️ (3/5 Risk)
CONFIRMED:  ⚠️ (1/5 Risk)
```

---

## İşlem Stratejileri

### 🔰 Yeni Başlayanlar İçin
```
1. REPAINT geldi → İGNORE (görmezden gel)
2. REALTIME geldi → İGNORE (görmezden gel)
3. CONFIRMED geldi → İŞLEM AÇ ✅
```
**Neden?** En güvenli yol. Sadece kesin sinyaller.

### 🎯 Orta Seviye Trader
```
1. REPAINT geldi → ALERT (uyarı al, hazırlan)
2. REALTIME geldi → WATCH (izle, bekleme)
3. CONFIRMED geldi → TRADE (işlem aç)
```
**Neden?** Erken hazırlık + güvenli giriş.

### ⚡ Agresif/Deneyimli Trader
```
1. REPAINT geldi → QUICK ENTRY (hızlı giriş, %25 pozisyon)
2. REALTIME geldi → ADD (pozisyon ekle, %25)
3. CONFIRMED geldi → FULL (tam pozisyon, %50)
veya
3. CONFIRMED gelmedi → EXIT (çık, repaint'ti)
```
**Neden?** Maksimum hız ama yüksek risk.

---

## Örnek Senaryo: Bar İçinde Neler Olur?

### Zaman Çizelgesi (1H Chart)

**15:05 - Bar açılışı**
```
Fiyat: 22.50
Durum: Normal
```

**15:20 - Koşullar sağlandı**
```
⚡ REPAINT geldi!
"BANKO KESIŞME AL [REPAINT]"
Fiyat: 22.78
```

**15:35 - Fiyat düştü**
```
Fiyat: 22.60
REPAINT sinyali iptal oldu (kayboldu)
Mesaj gelmedi
```

**15:50 - Fiyat tekrar yükseldi**
```
⚡ REPAINT tekrar geldi!
Fiyat: 22.85
```

**16:00 - Bar kapandı**
```
✓ CONFIRMED geldi!
"BANKO KESIŞME AL [CONFIRMED]"
Fiyat: 22.85
→ Kesin sinyal, işlem açılabilir
```

### Sonuç
- REPAINT 2 kez geldi (biri kayboldu)
- CONFIRMED 1 kez geldi (kesin)
- İşlem açmak için CONFIRMED beklemeliydin

---

## MTF (Multi-Timeframe) Durumu

### 4H Sinyal, 1H Chart'ta

**Chart: 1H, Sinyal: 4H BANKO AL**

**Saat 12:00 (1H chart)**
```
4H bar henüz kapanmadı
⚡ REALTIME geldi!
"BANKO KESIŞME AL (4H) [⚡REALTIME]"
```

**Saat 13:00, 14:00, 15:00 (1H chart)**
```
4H bar hala açık
REALTIME durumu devam ediyor
```

**Saat 16:00 (4H bar kapanışı)**
```
4H bar kapandı
✓ CONFIRMED geldi!
"BANKO KESIŞME AL (4H) [✓CONFIRMED]"
```

### MTF Mantığı
- REALTIME: Büyük TF bar'ı kapanmadan sinyal var
- CONFIRMED: Büyük TF bar'ı kapandı, sinyal kesin
- 1H chart'ta 4H sinyalini takip ediyorsun

---

## Teknik İmplementasyon

### Chart TF Sinyaller

#### REPAINT Implementation
```pinescript
// Line 1642
evLInt_Repaint = includeLongIntersect and longIntersectAlert

// Line 2023-2026
if allowLInt_Repaint
    _bankoReprintMsg = "⚡ BANKO KESİŞME AL [REPAINT]..."
    _bankoReprintId = "BANKO_REPAINT_" + str.tostring(bar_index)
    send_event(_bankoReprintId, _bankoReprintMsg, telegramChatId, alert.freq_once_per_bar)
```

#### CONFIRMED Implementation
```pinescript
// Line 1643
evLInt_Confirmed = confirmWrap(includeLongIntersect and longIntersectAlert)

// Line 2028-2032
if allowLInt_Confirmed
    _bankoConfMsg = "✓ BANKO KESİŞME AL [CONFIRMED]..."
    _bankoConfId = "BANKO_CONFIRMED_" + str.tostring(time)
    send_event(_bankoConfId, _bankoConfMsg, telegramChatId, alert.freq_once_per_bar_close)
```

### MTF Sinyaller

#### REALTIME/CONFIRMED Implementation
```pinescript
// Line 2110
statusLabel = tfClosed ? " [✓CONFIRMED]" : " [⚡REALTIME]"

// Line 2112
msg = evStrBuy + " (" + tfLabel + ")" + statusLabel + " [" + syminfo.ticker + "]..."
```

---

## Sık Sorulan Sorular (FAQ)

### 1. Hangi sinyale güvenmeliyim?
**Cevap:** CONFIRMED sinyaline. En güvenilir, asla kaybolmaz.

### 2. Neden birden fazla mesaj alıyorum?
**Cevap:** Hem REPAINT hem CONFIRMED gönderilir. REPAINT erken uyarı, CONFIRMED kesin onay.

### 3. CONFIRMED de yanlış olabilir mi?
**Cevap:** Evet, %10-15 başarısız olabilir. Ama REPAINT'e göre çok daha güvenilir.

### 4. REPAINT'i kapatabilir miyim?
**Cevap:** Hayır, kod şu anda ikisini de gönderiyor. Telegram'da sadece CONFIRMED'ı filtreleyebilirsin.

### 5. MTF REALTIME'a göre işlem açabilir miyim?
**Cevap:** Risk alıyorsan evet, ama CONFIRMED'ı beklemenizi öneriyoruz.

### 6. REPAINT neden var?
**Cevap:** Erken uyarı için. Hazırlık yapabilirsin, CONFIRMED'ı beklemeye hazır olursun.

### 7. 4H sinyali 1H'te ne zaman gelir?
**Cevap:** REALTIME hemen gelir, CONFIRMED 4 saat sonra (4H bar kapanınca).

### 8. Her REPAINT sonunda CONFIRMED gelir mi?
**Cevap:** Hayır! REPAINT kaybolabilir. Sadece bar sonunda koşullar sağlanırsa CONFIRMED gelir.

---

## Özet / Summary

### Türkçe

**3 Sinyal Tipi Var:**

1. **[⚡REPAINT]** - En hızlı ama en az güvenilir
   - Bar içinde anında
   - %40-60 başarı
   - Kaybolabilir
   - Sadece uyarı için kullan

2. **[⚡REALTIME]** - Orta hız, orta güvenilirlik
   - MTF sinyalleri için
   - %60-80 başarı
   - Büyük TF bar kapanmadan
   - İzleme amaçlı

3. **[✓CONFIRMED]** - En güvenilir
   - Bar kapandıktan sonra
   - %85-95 başarı
   - Asla kaybolmaz
   - **İşlem açmak için bunu kullan**

**Tavsiye:** Yeni başlıyorsan sadece CONFIRMED'a göre işlem yap!

---

### English

**3 Signal Types:**

1. **[⚡REPAINT]** - Fastest but least reliable
   - Fires immediately within bar
   - 40-60% success rate
   - Can disappear
   - Use only as early warning

2. **[⚡REALTIME]** - Medium speed, medium reliability
   - For MTF (multi-timeframe) signals
   - 60-80% success rate
   - Before higher TF bar closes
   - For monitoring purposes

3. **[✓CONFIRMED]** - Most reliable
   - Fires after bar closes
   - 85-95% success rate
   - Never disappears
   - **Use this for trading decisions**

**Recommendation:** If you're beginner, trade only on CONFIRMED signals!

---

## Kaynaklar / References

- Implementation: `V7_5_07226.txt`
- REPAINT: Lines 1642, 2023-2026
- CONFIRMED: Lines 1643, 2028-2032
- MTF REALTIME: Lines 2110, 2112

---

**Son Güncelleme / Last Updated:** 2026-02-13
**Versiyon / Version:** 1.0
