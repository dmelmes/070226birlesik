# MODÜL ÇALIŞMA REHBERİ

## İçindekiler
1. TURBO AL - 1-3 Günlük Momentum Sistemi
2. TURBO 2H - Intraday 2 Saatlik Sistem
3. FO (Forecast Oscillator) - Tahmin Osilatörü  
4. ALPHA (AlphaTrend) - Başarılı AlphaTrend Sistemi
5. BANKO KESIŞME AL - Çift EMA Kesişim Sistemi
6. ÇİFT DİP - Double Bottom Sistemi
7. HAFTALIK AL - Orta Vade Yüksek Getiri Sistemi

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

## 7. HAFTALIK AL - Orta Vade Yüksek Getiri Sistemi

### Ne İşe Yarar?
Haftalık veya aylık grafikte orta/uzun vadeli (haftalar-aylar) yüksek getirili fırsatları yakalar. %20-30 hedefli, dip seviyelerden giriş yapar ve hızlı hareket edecek hisseleri seçer.

### Nasıl Çalışır?

#### Temel Özellikler:
- **Timeframe:** Haftalık (W), Aylık (M), veya 2 Haftalık (2W) seçilebilir
- **Hedefler:** TP1 = %20, TP2 = %30
- **Stop Loss:** %8
- **Sinyal Sıklığı:** 1-3 sinyal/ay (çok seçici!)
- **Risk/Reward:** 2.5:1 ile 3.75:1 arası (mükemmel!)

### 11 Gelişmiş Filtre Sistemi

#### 1. Direnç Kontrolü (Overhead Resistance)
```pinescript
hafta_resistLookback = 50  // Son 50 bar kontrol edilir
hafta_resistTol = 2.0      // %2 tolerans

// Üstte direnç var mı?
for i = 1 to hafta_resistLookback
    hafta_priorHigh = hafta_h[i]
    if hafta_priorHigh > hafta_c and hafta_priorHigh <= hafta_upperLimit
        hafta_hasResist := true
        hafta_resistLevel := hafta_priorHigh
        break
```
**Anlamı:** Fiyatın üstünde %2 yakınında eski zirve var mı kontrol eder. Varsa "RESIST @145.00" gibi gösterir.

#### 2. Trend Filtresi (EMA Based)
```pinescript
hafta_trendLen = 50  // EMA 50 periyot
hafta_ema = ta.ema(hafta_c, hafta_trendLen)
hafta_trendUp = hafta_c > hafta_ema and hafta_ema > hafta_ema[1]
```
**Anlamı:** 
- Fiyat EMA(50)'nin ÜSTÜnde olmalı
- EMA yükseliyor olmalı (uptrend)

#### 3. RSI Filtresi - Geliştirilmiş Giriş Zamanlaması
```pinescript
hafta_rsiLen = 14
hafta_rsiMin = 55
hafta_rsi = ta.rsi(hafta_c, hafta_rsiLen)
hafta_rsiOK = hafta_rsi >= 50 and hafta_rsi <= 70  // Aşırı alımda değil
hafta_rsiRising = hafta_rsi > hafta_rsi[1]         // Momentum artıyor
```
**Anlamı:**
- RSI 50-70 arası (güçlü ama aşırı alımda değil)
- RSI yükseliyor (momentum var)

#### 4. Hacim Filtresi + Akümülasyon Tespiti
```pinescript
hafta_volMultiple = 1.5  // Hacim ortalamanın 1.5 katı
hafta_volAvg = ta.sma(hafta_v, 20)
hafta_volOK = hafta_v > hafta_volAvg * hafta_volMultiple

// Akümülasyon: Yukarı günlerde daha fazla hacim?
hafta_upVol = hafta_c > hafta_c[1] ? hafta_v : 0.0
hafta_dnVol = hafta_c < hafta_c[1] ? hafta_v : 0.0
hafta_upVolAvg = ta.sma(hafta_upVol, 5)
hafta_dnVolAvg = ta.sma(hafta_dnVol, 5)
hafta_isAccumulating = hafta_upVolAvg / hafta_dnVolAvg > 1.3
```
**Anlamı:**
- Hacim ortalamanın %50 üstünde
- Yukarı günlerde %30+ fazla hacim = AKÜMÜLASYON (akıllı para topluyor!)

#### 5. Güçlü Kapanış (Strong Close)
```pinescript
hafta_range = hafta_h - hafta_l
hafta_closeStrength = (hafta_c - hafta_l) / hafta_range
hafta_strongClose = hafta_closeStrength > 0.7  // Üst %30'da kapanış
```
**Anlamı:** Kapanış fiyatı bar'ın en üst %30'unda olmalı (alıcılar güçlü).

#### 6. Pullback Tespiti - DİP AL, TEPE DEĞIL! ⚠️ ÖNEMLİ
```pinescript
hafta_recentHigh = ta.highest(hafta_h, 10)  // Son 10 bar'ın zirvesi
hafta_pullbackPct = ((hafta_recentHigh - hafta_c) / hafta_recentHigh) * 100
hafta_isPullback = hafta_pullbackPct >= 2.0 and hafta_pullbackPct <= 20.0
```
**Anlamı:** 
- Son zirveye göre %2-20 geri çekilme olmalı
- Tepeden değil, DİPTEN AL!
- Mesaj: "PULLBACK -5.2%" gibi gösterir

#### 7. Destek Seviyesi Girişi ⚠️ ÖNEMLİ
```pinescript
hafta_support = ta.lowest(hafta_l, 50)  // Son 50 bar'ın dibi
hafta_distToSupport = ((hafta_c - hafta_support) / hafta_support) * 100
hafta_nearSupport = hafta_distToSupport <= 8.0  // Destekten %8 yakında
```
**Anlamı:**
- Destek seviyesinin %8 yakınında sinyal ver
- Güvenli giriş noktası
- Mesaj: "SUPPORT +2.9%" gibi gösterir

#### 8. Squeeze Tespiti - Patlama Yakın! ⚠️ ÖNEMLİ
```pinescript
hafta_bb_basis = ta.sma(hafta_c, 20)
hafta_bb_dev = ta.stdev(hafta_c, 20)
hafta_bb_width = (hafta_bb_dev / hafta_bb_basis) * 100  // Bollinger genişliği
hafta_bb_widthAvg = ta.sma(hafta_bb_width, 20)
hafta_isSqueezed = hafta_bb_width < hafta_bb_widthAvg * 0.75
```
**Anlamı:**
- Bollinger Band genişliği ortalamanın %75'inden az
- SIKIŞIK = Düşük volatilite = PATLAMA YAKINDA!
- Mesaj: "SQUEEZE" gösterir

#### 9. Momentum Onayı - Yükselen Dipler
```pinescript
hafta_higherLow = hafta_l > hafta_l[1] and hafta_l[1] > hafta_l[2]
hafta_recentGain = ((hafta_c - hafta_c[3]) / hafta_c[3]) * 100
hafta_hasStrength = hafta_recentGain >= 1.5  // Son 3 bar'da %1.5+ kazanç
```
**Anlamı:**
- Higher lows (yükselen dipler) = Boğa yapısı
- Son 3 bar'da %1.5+ kazanç = Güç var
- Mesaj: "HL-MOMENTUM" gösterir

#### 10. Breakout veya Açık Yol
```pinescript
hafta_highest = ta.highest(hafta_h, 50)
hafta_isBreakout = hafta_c >= hafta_highest * 0.98  // Zirveye %2 yakın
hafta_clearPath = not hafta_hasResist or hafta_isBreakout
```
**Anlamı:**
- Ya üstte direnç YOK
- Ya da direnç KIRIYOR
- Mesaj: "BREAKOUT" veya "CLEAR PATH" gösterir

#### 11. Cooldown (Aşırı Sinyal Engelleme)
```pinescript
hafta_cooldown = 10  // Minimum 10 bar ara
hafta_cooldownOK = na(hafta_lastBar) or (bar_index - hafta_lastBar) >= hafta_cooldown
```
**Anlamı:** Aynı hisseden 10 bar (10 hafta) içinde tekrar sinyal vermez.

### GELİŞMİŞ FİLTRE KOMBİNASYONU

#### 3 Katmanlı Sistem:

**1. Çekirdek Filtreler (MUTLAKA GEREKLİ):**
```pinescript
hafta_coreFilters = hafta_trendUp and 
                    hafta_rsiOK and 
                    hafta_rsiRising and 
                    hafta_volOK and 
                    hafta_strongClose and 
                    hafta_cooldownOK
```

**2. Giriş Kalitesi (EN AZ 1 TANESİ):**
```pinescript
hafta_goodEntry = hafta_isPullback or hafta_nearSupport
```
- Ya pullback (dip) olmalı
- Ya destek yakını olmalı
- İKİSİNDEN BİRİ YETER!

**3. Hareket Hazırlığı (EN AZ 1 TANESİ):**
```pinescript
hafta_readyToMove = hafta_isAccumulating or 
                    hafta_isSqueezed or 
                    (hafta_higherLow and hafta_hasStrength)
```
- Ya akümülasyon var
- Ya squeeze var
- Ya momentum var
- BİRİ YETER!

**FINAL SİNYAL:**
```pinescript
hafta_allFilters = hafta_coreFilters and 
                   hafta_goodEntry and 
                   hafta_readyToMove and 
                   hafta_pathOK
```

### Mesaj Formatı

```
🚀 HAFTALIK AL|THYAO
|PULLBACK -5.2%           ← Giriş kalitesi (dip seviyeden!)
|E=142.50                 ← Entry fiyat
|SL=131.10 (-8%)          ← Stop loss
|TP1=171.00 (+20%)        ← Hedef 1
|TP2=185.25 (+30%)        ← Hedef 2
|RSI=65                   ← RSI değeri
|CLEAR PATH               ← Üstte direnç durumu
|VOL=2.3x                 ← Hacim durumu
|SQUEEZE                  ← Hareket sinyali (patlama yakın!)
```

**Mesajdan Anlayacağınız:**
- **PULLBACK -5.2%:** Tepeden %5.2 geri çekildi, DİPTEN alıyoruz! ✅
- **SQUEEZE:** Hisse sıkışık, PATLAMA YAKINDA! ✅
- **CLEAR PATH:** Üstte direnç yok, YOL AÇIK! ✅

### Örnek Senaryolar

#### Senaryo 1: Mükemmel Setup
```
- Trend ✓
- RSI 65, yükseliyor ✓
- Hacim 2.5x ✓
- Güçlü kapanış ✓
- Pullback %6 ✓ (Giriş kalitesi!)
- Squeeze var ✓ (Hareket hazır!)
- Clear path ✓

SONUÇ: ✅ SİNYAL VERİR!
Mesaj: "PULLBACK -6.0%|SQUEEZE"
```

#### Senaryo 2: Trend Başlangıcı
```
- Trend ✓
- RSI 67, yükseliyor ✓
- Hacim 1.8x ✓
- Güçlü kapanış ✓
- Pullback yok ❌
- Destek yakını ✓ (Giriş kalitesi!)
- Akümülasyon ✓ (Hareket hazır!)
- Breakout ✓

SONUÇ: ✅ SİNYAL VERİR!
Mesaj: "SUPPORT +3.5%|ACCUM|BREAKOUT"
```

#### Senaryo 3: Yatay Hareket (Filtrelenir)
```
- Trend ✓
- RSI 58, yükseliyor ✓
- Hacim 1.6x ✓
- Güçlü kapanış ✓
- Pullback yok ❌
- Destek uzakta ❌
- Squeeze yok ❌
- Akümülasyon yok ❌
- Momentum yok ❌

SONUÇ: ❌ SİNYAL VERMEZ!
Sebep: Giriş kalitesi YOK ve Hareket hazırlığı YOK
```

### Beklenen Performans

**Sıklık:** 1-3 sinyal/ay (100 hisse üzerinde)
- Çok seçici!
- Ama çok kaliteli!

**Başarı Oranı:** %60-70 (beklenen)
- Yüksek hedefler (%20-30)
- İyi risk/reward (2.5-3.75:1)

**Hareket Süresi:**
- İlk %10 hareket: 2-4 hafta
- TP1 (%20): 1-3 ay
- TP2 (%30): 2-6 ay

### Ne Zaman Kullanmalı?

**Uygun:**
- ✅ Orta/uzun vade yatırım
- ✅ Yüksek getiri hedefi (%20-30)
- ✅ Haftalar/aylar tutabilirsin
- ✅ Az ama kaliteli sinyal istiyorsun

**Uygun Değil:**
- ❌ Günlük trading
- ❌ Hızlı kar al-sat
- ❌ Çok sık sinyal istiyorsun

### Kod Konumu

**Parametreler:** Lines 2198-2212  
**Ana Mantık:** Lines 2218-2320  
**Enable Durumu:** `hafta_enable = true` ✅ Line 2199

### Önemli Notlar

1. **Timeframe Seçimi:**
   - W (haftalık): En popüler, dengeli
   - M (aylık): Çok uzun vade, az sinyal
   - 2W (2 haftalık): Orta yol

2. **Giriş Kalitesi ÖNEMLİ:**
   - Pullback VEYA destek (en az 1)
   - TEPEDEN ALMA!

3. **Hareket Tahminleme ÖNEMLİ:**
   - Squeeze/akümülasyon/momentum (en az 1)
   - Hisse HAZIR olmalı hareket etmeye!

4. **Sabır Gerekli:**
   - Ayda 1-3 sinyal normal
   - Kalite > Kantite

---

## Tüm Modüller Aktif!

```pinescript
dt_enable = true           ✅ Line 2052
fo_enable = true           ✅ Line 2088
turbo_enable = true        ✅ Line 2329
turbo2h_enable = true      ✅ Line 2423
enableAlphaPerf = true     ✅ Line 2508
hafta_enable = true        ✅ Line 2199  ← YENİ!
```

**HEPSİ ÇALIŞIYOR!** 🚀
