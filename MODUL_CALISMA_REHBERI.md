# MODÜL ÇALIŞMA REHBERİ

## İçindekiler
1. TURBO AL - 1-3 Günlük Momentum Sistemi
2. TURBO 2H - Intraday 2 Saatlik Sistem
3. FO (Forecast Oscillator) - Tahmin Osilatörü  
4. ALPHA (AlphaTrend) - Başarılı AlphaTrend Sistemi
5. BANKO KESIŞME AL - Çift EMA Kesişim Sistemi
6. ÇİFT DİP - Double Bottom Sistemi

---

## 1. TURBO AL - 1-3 Günlük Momentum Sistemi

### Ne İşe Yarar?
Kısa vadeli (1-3 gün) güçlü momentum hareketlerini yakalar. Hacim patlaması, RSI momentum ve fiyat breakout'u birleştiğinde sinyal verir.

### Nasıl Çalışır?

#### A. Filtreler (Hepsi Gerekli):

**1. Hacim Filtresi (Volume Filter)**
```pinescript
turbo_volMultiple = 2.0  // Hacim ortalamanın 2 katı olmalı
turbo_vol5DayMax = 1.5   // Son 5 günün max hacminin 1.5 katı olmalı

turbo_volAvg = ta.sma(volume, 20)
turbo_volMax5 = ta.highest(volume, 5)
turbo_volFilter = volume > turbo_volMultiple * turbo_volAvg and 
                  volume > turbo_volMax5 * turbo_vol5DayMax
```
**Anlamı:** Hacimde PATLAMA olmalı! Hem ortalamadan hem son 5 günden çok daha fazla.

**2. Momentum Filtresi (RSI)**
```pinescript
turbo_rsi14Thresh = 50    // RSI 14 periyot 50'yi geçmeli
turbo_rsi7Thresh = 65     // RSI 7 periyot 65'te olmalı

turbo_rsi14 = ta.rsi(close, 14)
turbo_rsi7 = ta.rsi(close, 7)
turbo_rsiCross = ta.crossover(turbo_rsi14, turbo_rsi14Thresh)
turbo_momentumFilter = turbo_rsiCross and 
                       turbo_rsi7 > turbo_rsi7Thresh and
                       close > turbo_ema21
```
**Anlamı:** 
- RSI(14) 50'yi yukarı kesmeli (momentum değişimi)
- RSI(7) 65'te olmalı (kısa vadede güçlü)
- Fiyat EMA(21)'in üstünde (trend yukarı)

**3. Breakout Filtresi**
```pinescript
turbo_breakoutLen = 10   // 10 günlük en yüksek seviye

turbo_highest = ta.highest(high, turbo_breakoutLen)
turbo_range = high - low
turbo_atr = ta.atr(14)
turbo_wideRange = turbo_range > turbo_breakoutAtrMult * turbo_atr

turbo_breakoutFilter = close > turbo_highest and 
                       close > open and
                       turbo_wideRange
```
**Anlamı:** 
- Fiyat 10 günlük en yüksek seviyeyi kırmalı
- Mum yeşil olmalı (close > open)
- Geniş range olmalı (1.5 x ATR)

#### B. Sinyal Oluşumu:
```pinescript
turbo_signal = turbo_volFilter and turbo_momentumFilter and turbo_breakoutFilter
```
**HER ÜÇ FİLTRE DE AYNI ANDA TRUE OLMALI!**

#### C. Hedef ve Stop:
```pinescript
Hedef 1 (TP1): %15-20 yukarı
Hedef 2 (TP2): %25-30 yukarı  
Stop Loss: En düşük seviyenin %2-3 altı
```

### Ne Zaman Sinyal Verir?
- Hacim PATLADI (2x ortalama)
- RSI momentum güçlü (50 cross + 65)
- Fiyat breakout yaptı (10 gün high kırdı)

**Örnek:** THYAO hissesi sessiz kalmış, bir anda hacim patladı, RSI 50'yi geçti, fiyat da 10 günlük en yükseği kırdı → TURBO AL sinyali!

### Sıklık:
1-5 sinyal/ay (100 hisse için) - ÇOK SEÇİCİ!

---

## 2. TURBO 2H - Intraday 2 Saatlik Sistem

### Ne İşe Yarar?
Gün içi (intraday) 2 saatlik grafikte hızlı alım-satım fırsatlarını yakalar. TURBO AL'ın daha gevşek versiyonu.

### Nasıl Çalışır?

#### A. Filtreler (TURBO AL'dan daha gevşek):

**1. Hacim Filtresi**
```pinescript
turbo2h_volMultiple = 1.5  // 1.5x (TURBO AL'da 2.0x)
turbo2h_vol5DayMax = 1.3   // 1.3x (TURBO AL'da 1.5x)

turbo2h_volFilter = volume > turbo2h_volMultiple * turbo2h_volAvg and
                    volume > turbo2h_vol5DayMax * turbo2h_volMax5
```
**Anlamı:** Hacim artışı yeterli ama TURBO AL kadar sert değil.

**2. Momentum Filtresi**
```pinescript
turbo2h_rsi14Thresh = 50   // Aynı
turbo2h_rsi7Thresh = 60    // 60 (TURBO AL'da 65)

turbo2h_momentumFilter = turbo2h_rsi14 > turbo2h_rsi14Thresh and
                         turbo2h_rsi7 > turbo2h_rsi7Thresh and
                         close > turbo2h_ema21
```
**Anlamı:** 
- RSI(14) > 50 olmalı (cross değil, sadece üstünde)
- RSI(7) > 60 (TURBO AL'dan daha düşük)

**3. Breakout Filtresi**
```pinescript
turbo2h_breakoutLen = 7    // 7 saat (TURBO AL'da 10)

turbo2h_breakoutFilter = close > turbo2h_highest and
                         close > open and
                         turbo2h_wideRange
```
**Anlamı:** 7 saatlik (14 bar, her bar 2h) yüksek kırmalı.

#### B. Hedef ve Stop:
```pinescript
Hedef 1: %8-12
Hedef 2: %15-20
Stop Loss: %3-5
```

### TURBO AL vs TURBO 2H Farkları:

| Özellik | TURBO AL | TURBO 2H |
|---------|----------|----------|
| **Timeframe** | 1 gün | 2 saat |
| **Hedef** | 1-3 gün | Birkaç saat-1 gün |
| **Hacim** | 2.0x çok sert | 1.5x orta |
| **RSI7** | 65 çok yüksek | 60 orta |
| **Breakout** | 10 gün | 7 bar (14 saat) |
| **Sıklık** | 1-5/ay | 5-15/ay |
| **Kalite** | Çok yüksek | Yüksek |

### Ne Zaman Kullanılır?
- **TURBO AL:** Haftalık swing trade, büyük hedefler
- **TURBO 2H:** Günlük trading, hızlı giriş-çıkış

---

## 3. FO (Forecast Oscillator) - Tahmin Osilatörü

### Ne İşe Yarar?
Linear regression (doğrusal regresyon) kullanarak fiyatın geleceğini tahmin eder. Tahmin yukarıysa ve diğer filtreler uygunsa AL sinyali verir.

### Nasıl Çalışır?

#### A. Forecast Oscillator Hesaplaması:
```pinescript
fo_len = 14  // Linear regression uzunluğu

// Linear regression tahmin
fo_linreg = ta.linreg(close, fo_len, 0)

// Forecast oscillator
fo_osc = ((close - fo_linreg) / close) * 100
```
**Anlamı:** 
- LinReg: Son 14 bar'ın trend çizgisi
- FO: Fiyatın trend çizgisine göre konumu
- Pozitif = Fiyat trendin üstünde

#### B. Sinyal Filtresi:
```pinescript
fo_crossover = ta.crossover(fo_osc, 0)  // FO 0'ı yukarı kesmeli

// Trend filtresi
fo_trendUp = fo_linreg > fo_linreg[1]  // LinReg yükseliyor olmalı

// RSI filtresi  
fo_rsiMin = 50
fo_rsiOK = fo_rsi > fo_rsiMin and fo_rsi > fo_rsi[1]

// Hacim filtresi
fo_volFilter = volume > ta.sma(volume, 20) * 1.2

// XU100 filtresi (opsiyonel)
fo_xuOK = not fo_xu100Filter or xu100_trend > 0
```

#### C. Geliştirilmiş Hedefler:
```pinescript
// R-multiple hedefler
fo_rr1 = 2.5  // Target 1 = 2.5R
fo_rr2 = 4.0  // Target 2 = 4.0R

// Minimum % hedefler
fo_minTarget1Pct = 8.0   // En az %8
fo_minTarget2Pct = 15.0  // En az %15

// Stop loss
fo_stop = close - fo_atr * fo_atrStopMult

// Hedefler (ikisinden büyüğü)
fo_risk = close - fo_stop
fo_target1_r = close + (fo_risk * fo_rr1)
fo_target1_pct = close * (1 + fo_minTarget1Pct / 100)
fo_target1 = math.max(fo_target1_r, fo_target1_pct)

fo_target2_r = close + (fo_risk * fo_rr2)
fo_target2_pct = close * (1 + fo_minTarget2Pct / 100)
fo_target2 = math.max(fo_target2_r, fo_target2_pct)
```

**Anlamı:**
- ATR-based hedef VEYA sabit % hedef
- İkisinden BÜYÜĞÜ kullanılır
- Garantili minimum %8 ve %15 hedefler!

### Sinyal Örneği:
```
FO_AL|GARAN|TF=4H|Fiyat=31.50
TP1=34.02 (+8.0%) | TP2=36.23 (+15.0%)
SL=30.21 (-4.1%)
```

### Sıklık:
3-10 sinyal/ay - Orta sıklık

---

## 4. ALPHA (AlphaTrend) - Başarılı AlphaTrend Sistemi

### Ne İşe Yarar?
ATR-based trend takip sistemi + HİSTORİK BAŞARI FİLTRESİ. Geçmişteki kazanç oranına bakarak sadece başarılı sinyalleri filtreler!

### Nasıl Çalışır?

#### A. AlphaTrend Hesaplaması:
```pinescript
alpha_atrLen = 14
alpha_atrMult = 1.0

alpha_atr = ta.atr(alpha_atrLen)
alpha_upT = (high + low) / 2 - alpha_atrMult * alpha_atr
alpha_downT = (high + low) / 2 + alpha_atrMult * alpha_atr

var float alpha_trend = na
alpha_trend := close > alpha_trend[1] ? math.max(alpha_upT, alpha_trend[1]) : 
               close < alpha_trend[1] ? math.min(alpha_downT, alpha_trend[1]) : 
               alpha_trend[1]

// Trend değişimi
alpha_buySignal = ta.crossover(close, alpha_trend)
alpha_sellSignal = ta.crossunder(close, alpha_trend)
```

**Anlamı:** 
- Fiyat alpha_trend çizgisini yukarı keserse → AL
- Fiyat alpha_trend çizgisini aşağı keserse → SAT

#### B. Historik Performans Filtresi (ÖZEL!):
```pinescript
alpha_histMinSamples = 20       // En az 20 sinyal gerekli
alpha_histWinRateMin = 0.55     // %55 kazanma oranı gerekli
alpha_gateWhenInsufficient = "Pass"  // Az data varsa geçir

// Performans kaydı
var array<float> alpha_hist_entries = array.new_float()
var array<float> alpha_hist_exits = array.new_float()
var array<bool> alpha_hist_won = array.new_bool()

// AL sinyalinde kaydet
if alpha_buySignal
    array.push(alpha_hist_entries, close)
    array.push(alpha_hist_exits, na)
    array.push(alpha_hist_won, na)

// SAT sinyalinde kapat ve kazan/kaybet hesapla
if alpha_sellSignal and array.size(alpha_hist_entries) > 0
    last_entry = array.get(alpha_hist_entries, array.size(alpha_hist_entries) - 1)
    profit = (close - last_entry) / last_entry
    won = profit > 0
    array.set(alpha_hist_won, array.size(alpha_hist_won) - 1, won)

// Win rate hesapla
total_trades = 0
wins = 0
for i = 0 to array.size(alpha_hist_won) - 1
    if not na(array.get(alpha_hist_won, i))
        total_trades += 1
        if array.get(alpha_hist_won, i)
            wins += 1

win_rate = total_trades > 0 ? wins / total_trades : 0

// Filtre
alpha_histOK = (total_trades < alpha_histMinSamples and alpha_gateWhenInsufficient == "Pass") or
               (total_trades >= alpha_histMinSamples and win_rate >= alpha_histWinRateMin)
```

**Anlamı:**
1. İlk 20 sinyal → Hepsine izin ver (öğrenme fazı)
2. 20+ sinyal sonra → Sadece %55+ kazanma oranı varsa izin ver
3. Zayıf performanslı hisselerde sinyal vermez!

#### C. Multi-Timeframe:
```pinescript
alpha_mtf = "4H"  // 4 saatlik timeframe kontrol

[alpha_mtf_close, alpha_mtf_trend, alpha_mtf_signal] = 
    request.security(syminfo.tickerid, alpha_mtf, 
                     [close, alpha_trend, alpha_buySignal])

// MTF onay
alpha_mtfOK = not alpha_enableMTF or alpha_mtf_close > alpha_mtf_trend
```

### Ne Zaman Sinyal Verir?
- Fiyat AlphaTrend çizgisini yukarı kesti
- Geçmiş kazanma oranı %55+
- MTF de pozitif (opsiyonel)

### Sıklık:
2-8 sinyal/ay - İlk 20 sinyal sonra daha seçici olur!

---

## 5. BANKO KESIŞME AL - Çift EMA Kesişim Sistemi

### Ne İşe Yarar?
Hızlı EMA ve Yavaş EMA kesişimini kullanarak trend değişimlerini yakalar. Ek olarak hacim, momentum ve volatilite analizi yapar.

### Nasıl Çalışır?

#### A. Dual SuperTrend + EMA Sistemi:
```pinescript
// SuperTrend hesaplaması
st_atr = ta.atr(st_atrLen)
st_upLine = hl2 - st_atrMult * st_atr
st_dnLine = hl2 + st_atrMult * st_atr

var int st_dir = 1
st_dir := st_dir == -1 and close > st_dnLine ? 1 : 
          st_dir == 1 and close < st_upLine ? -1 : st_dir

// EMA'lar
ema_fast = ta.ema(close, emaFastLen)  // 21
ema_slow = ta.ema(close, emaSlowLen)  // 55

// BANKO kesişimi
banko_longIntersect = st_dir == 1 and st_dir[1] == -1 and 
                      ema_fast > ema_slow and
                      close > ema_fast
```

**Anlamı:**
- SuperTrend yukarı dönmeli (bearish → bullish)
- Hızlı EMA > Yavaş EMA (trend up)
- Fiyat > Hızlı EMA (güçlü)

#### B. Gelişmiş Analitikler:
```pinescript
// Hacim analizi
banko_volAvg = ta.sma(volume, 20)
banko_volRatio = volume / banko_volAvg
banko_volPct = ((banko_volRatio - 1.0) * 100)

banko_volText = banko_volRatio > 1.5 ? "GÜÇLÜ (+%...) ✅" :
                banko_volRatio > 1.0 ? "VAR (+%...) ✅" :
                banko_volRatio > 0.8 ? "ORTA (%...) ⚠️" :
                "ZAYIF (%...) ❌"

// Momentum analizi (RSI)
banko_rsi = ta.rsi(close, 14)
banko_momText = banko_rsi > 60 ? "GÜÇLÜ (RSI 60+) ✅" :
                banko_rsi > 50 ? "ORTA (RSI 50-60) ⚠️" :
                "ZAYIF (RSI <50) ❌"

// Volatilite analizi (ATR)
banko_atr = ta.atr(14)
banko_atrPct = (banko_atr / close) * 100
banko_volText2 = banko_atrPct > 4.0 ? "YÜKSEK ⚡" :
                 banko_atrPct > 2.0 ? "ORTA 📊" :
                 "DÜŞÜK 😴"

// Güç skoru
banko_score = 0
if banko_volRatio > 2.0 then banko_score += 3
else if banko_volRatio > 1.5 then banko_score += 2
else if banko_volRatio > 1.2 then banko_score += 1

if banko_rsi > 60 then banko_score += 2
else if banko_rsi > 55 then banko_score += 1

if banko_atrPct > 3.0 then banko_score += 1

banko_grade = banko_score >= 5 ? "A+ ⭐⭐⭐" :
              banko_score >= 3 ? "B ⭐⭐" :
              "C ⭐"
```

#### C. Mesaj Formatı:
```
✓ BANKO KESIŞME AL [CONFIRMED]
[NTGAZ] [4H]
Fiyat: 12.30

📊 Analiz:
Hacim: GÜÇLÜ (+85%) ✅
Momentum: GÜÇLÜ (RSI 67 ↑) ✅
Volatilite: ORTA 📊
Güç: A+ ⭐⭐⭐

✅ Kesin sinyal - Bar kapatıldı
```

### Çalışma Mantığı Detay:

1. **Kesişim tespit edilir** (SuperTrend + EMA)
2. **Bar kapatılır** (confirmed)
3. **Analitikler hesaplanır:**
   - Hacim durumu
   - Momentum (RSI)
   - Volatilite (ATR)
   - Güç skoru (A+, B, C)
4. **Mesaj gönderilir** (Telegram)

### Sorun Giderme:
Eğer "HESAPLANIYOR" veya "VERİ YOK" görüyorsan:
- İlk 20-30 bar'da normal (yeterli data yok)
- Sonrasında görüyorsan kod hatası var

---

## 6. ÇİFT DİP (Double Bottom) - DT Modülü

### Ne İşe Yarar?
Klasik çift dip formasyonunu (W pattern) otomatik tespit eder.

### Nasıl Çalışır?

#### A. Pivot Low Tespiti:
```pinescript
dt_pivotLen = 14  // Sol ve sağ bar sayısı

dt_pl = ta.pivotlow(low, dt_pivotLen, dt_pivotLen)
```
**Anlamı:** 14 bar solunda ve sağında kendinden yüksek kapanış varsa → pivot low

#### B. Çift Dip Arama:
```pinescript
dt_tolerance = 2.0  // %2 tolerans
dt_lookback = 30    // 30 bar geriye bak

if not na(dt_pl)  // Yeni pivot low oluştu
    // 30 bar geriye git, benzer pivot ara
    for i = dt_pivotLen + 1 to dt_lookback
        old_pivot = low[i]
        diff_pct = math.abs((dt_pl - old_pivot) / old_pivot) * 100
        
        if diff_pct <= dt_tolerance
            // Benzer dip bulundu!
            if close > dt_pl  // Fiyat dibin üstünde
                dt_confDB = true  // ÇİFT DİP ONAY!
```

**Anlamı:**
1. Yeni pivot low oluşur
2. Geriye 30 bar bakılır
3. %2 toleransta benzer pivot varsa → Çift dip!
4. Fiyat dibin üstündeyse → AL sinyali

#### C. Mesaj:
```
DT ÇİFT DİP AL|THYAO|TF=1H|Fiyat=142.50
```

### Sıklık:
1-3 sinyal/ay - Çift dip formasyonu nadir!

### Durum:
```pinescript
Line 2052: dt_enable = true  ✅ AKTİF!
```

---

## Özet Karşılaştırma

| Modül | Amaç | Timeframe | Sıklık | Kalite |
|-------|------|-----------|--------|--------|
| **TURBO AL** | 1-3 günlük momentum | 1D | 1-5/ay | Çok yüksek |
| **TURBO 2H** | Intraday hızlı | 2H | 5-15/ay | Yüksek |
| **FO** | Trend tahmin | 1H-4H | 3-10/ay | Yüksek |
| **ALPHA** | Trend + history | 4H | 2-8/ay | Çok yüksek |
| **BANKO** | EMA kesişim | 4H | 3-10/ay | Yüksek |
| **ÇİFT DİP** | Pattern | 1H-4H | 1-3/ay | Yüksek |

---

## Tüm Modüller Aktif!

```pinescript
dt_enable = true           ✅ Line 2052
fo_enable = true           ✅ Line 2088
turbo_enable = true        ✅ Line 2329
turbo2h_enable = true      ✅ Line 2423
enableAlphaPerf = true     ✅ Line 2508
```

**HEPSİ ÇALIŞIYOR!** 🚀
