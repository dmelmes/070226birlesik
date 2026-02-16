# ✅ EMA Modülü - Watchlist Kaldırıldı (Diğer Modüller Gibi)

## 🔄 Ne Değişti?

### Önceki Durum (Yanlış Anlaşılma!)
- EMA modülü **sabit sembol listesi** kullanıyordu
- Örnek: `THYAO,PETKM,SASA,SAHOL,AKBNK...` (10 sembol)
- Her sembol için `request.security()` çağrısı yapıyordu
- **Sorunlar:**
  - Request.security limiti aşma riski
  - Karmaşık kod
  - Esnek olmayan yapı

### Yeni Durum (Doğru!)
- EMA modülü **sadece açık grafikteki hisse** için çalışır
- SuperDip, Pullback, E2 gibi diğer modüller ile aynı
- Kullanıcı hangi hisseyi açarsa o hisse için sinyal verir
- **Avantajlar:**
  - Basit ve anlaşılır
  - Request.security limiti sorunu yok
  - TradingView'un kendi alert sistemi ile uyumlu

---

## 📋 Kaldırılan Özellikler

### Input'lar (Artık Yok)
- ❌ `ema_watch_enable` - Watchlist tarama aktif/pasif
- ❌ `ema_watch_prefix` - Sembol prefix (örn: BIST:)
- ❌ `ema_watch_symbols` - Sembol listesi
- ❌ `ema_watch_buy_chat_id` - Watchlist BUY chat ID
- ❌ `ema_watch_sell_chat_id` - Watchlist SELL chat ID
- ❌ `grpEMAWatch` - Watchlist grubu

### Fonksiyonlar (Artık Yok)
- ❌ `f_ema_parse_symbols()` - Sembol parsing fonksiyonu
- ❌ `f_ema_check_symbol()` - Sembol kontrol fonksiyonu
- ❌ Watchlist tarama kodu (120+ satır)

### Mesajlar (Artık Yok)
- ❌ Toplu BUY mesajı: `⚡ EMA CROSS 1H TARAMA • BUY (AL)`
- ❌ Toplu SELL mesajı: `⚡ EMA CROSS 1H TARAMA • SELL (SAT)`

---

## ✅ Kalan Özellikler (Aktif!)

### Input'lar
- ✅ `ema_enable` - EMA modülü aktif/pasif
- ✅ `ema_fast` - Hızlı EMA (varsayılan: 5)
- ✅ `ema_slow` - Yavaş EMA (varsayılan: 137)
- ✅ `ema_enable_buy` - BUY sinyalleri aktif
- ✅ `ema_enable_sell` - SELL sinyalleri aktif (varsayılan: kapalı)
- ✅ `ema_buy_chat_id` - BUY Telegram chat ID
- ✅ `ema_sell_chat_id` - SELL Telegram chat ID
- ✅ `ema_cooldown_min` - Cooldown süresi (varsayılan: 60 dk)
- ✅ `ema_show_labels` - Grafikte label göster

### Sinyaller
- ✅ **BUY Signal:** 1H EMA5 yukarı kesti EMA137 + 15m EMA5 > EMA137
- ✅ **SELL Signal:** 1H EMA5 aşağı kesti EMA137 + 15m EMA5 < EMA137

### Alert'ler
- ✅ `alertcondition(ema_buy_signal)` - EMA CROSS BUY (1H+15m)
- ✅ `alertcondition(ema_sell_signal)` - EMA CROSS SELL (1H+15m)

### Mesajlar
- ✅ Tek hisse BUY mesajı: `⚡ EMA CROSS 1H • BUY (AL)`
- ✅ Tek hisse SELL mesajı: `⚡ EMA CROSS 1H • SELL (SAT)`

---

## 🎯 Nasıl Kullanılır?

### Adım 1: TradingView'a Script'i Yükleyin
1. Pine Editor'u açın (Alt+E)
2. `Pullbackformasyon ve dip_v7.txt` dosyasını kopyalayın
3. Yapıştırın ve "Kaydet"
4. "Grafiğe Ekle"

### Adım 2: İzlemek İstediğiniz Hisseyi Açın
Örnek:
- BIST:THYAO için → THYAO grafiğini açın
- BIST:PETKM için → PETKM grafiğini açın
- BIST:SASA için → SASA grafiğini açın

### Adım 3: Alert Kurun (TradingView Özelliği)
1. **Alert oluştur** (⏰ ikonu)
2. **Condition** seçin:
   - "EMA CROSS BUY (1H+15m)" veya
   - "EMA CROSS SELL (1H+15m)"
3. **Alert name** girin (örn: "THYAO EMA BUY")
4. **Notifications** seçin:
   - ✓ App/Webhook
   - ✓ Email (opsiyonel)
5. **Create**

### Adım 4: Her Hisse İçin Tekrarlayın
- TradingView'da her hisse için **ayrı alert** kurabilirsiniz
- Örnek:
  - Alert 1: THYAO - EMA CROSS BUY
  - Alert 2: PETKM - EMA CROSS BUY
  - Alert 3: SASA - EMA CROSS BUY
  - ...

---

## 💡 Örnek Kullanım Senaryosu

### Senaryo: 5 Hisseyi İzlemek İstiyorsunuz

**Hisseler:** THYAO, PETKM, SASA, AKBNK, EREGL

**Yöntem:**

1. **THYAO grafiğini açın** → Alert kurun → "THYAO EMA BUY"
2. **PETKM grafiğini açın** → Alert kurun → "PETKM EMA BUY"
3. **SASA grafiğini açın** → Alert kurun → "SASA EMA BUY"
4. **AKBNK grafiğini açın** → Alert kurun → "AKBNK EMA BUY"
5. **EREGL grafiğini açın** → Alert kurun → "EREGL EMA BUY"

**Sonuç:**
- ✅ 5 hisse için 5 ayrı alert
- ✅ Her alert sadece o hisse için tetiklenir
- ✅ Telegram'a mesaj gider
- ✅ TradingView notification alırsınız

---

## 📱 Mesaj Formatı

### BUY Mesajı (Tek Hisse)
```
⚡ EMA CROSS 1H • BUY (AL)
HISSE: THYAO | FIYAT: 315.50

TETİK: 1H EMA5 yukarı kesti EMA137
ONAY: 15m EMA5 > EMA137 (STATE)

1H EMA5: 315.50
1H EMA137: 310.00
15m EMA5: 316.00
15m EMA137: 311.00
```

### SELL Mesajı (Tek Hisse)
```
⚡ EMA CROSS 1H • SELL (SAT)
HISSE: THYAO | FIYAT: 308.00

TETİK: 1H EMA5 aşağı kesti EMA137
ONAY: 15m EMA5 < EMA137 (STATE)

1H EMA5: 308.00
1H EMA137: 310.00
15m EMA5: 307.50
15m EMA137: 309.00
```

---

## 🔧 Ayarlar

### Temel Ayarlar (Satır 143-152)
```pinescript
ema_enable=input.bool(true,"EMA Cross Modülü Aktif",group=grpEMA)
ema_fast=input.int(5,"EMA Fast (Hızlı)",minval=1,group=grpEMA)
ema_slow=input.int(137,"EMA Slow (Yavaş)",minval=1,group=grpEMA)
ema_enable_buy=input.bool(true,"BUY Sinyalleri Aktif",group=grpEMA)
ema_enable_sell=input.bool(false,"SELL Sinyalleri Aktif",group=grpEMA)
ema_buy_chat_id=input.string("-1002781417418","EMA BUY chat_id",group=grpEMA)
ema_sell_chat_id=input.string("-1002587291984","EMA SELL chat_id",group=grpEMA)
ema_cooldown_min=input.int(60,"EMA Cooldown (dk)",minval=0,group=grpEMA)
ema_show_labels=input.bool(true,"EMA Label Göster",group=grpEMA)
```

### TradingView Ayarlarından Değiştirme
1. Gösterge → Ayarlar (⚙️)
2. "EMA Cross (1H + 15m Onay)" grubunu bulun
3. Değerleri düzenleyin
4. Tamam → Kaydet

---

## ❓ Sık Sorulan Sorular

### S: Watchlist tarama neden kaldırıldı?
**C:** Kullanıcı isteği üzerine. Diğer modüller (SuperDip, Pullback) gibi çalışması için. Ayrıca request.security limiti sorunu tamamen çözüldü.

### S: Birden fazla hisseyi nasıl takip ederim?
**C:** Her hisse için ayrı grafik açıp ayrı alert kurarsınız. TradingView'un standart yöntemi bu şekilde.

### S: Eski watchlist taramasını geri getirebilir miyim?
**C:** Hayır. Kod tamamen kaldırıldı. Ama TradingView alert sistemi ile aynı işlevselliği elde edebilirsiniz.

### S: Her hisse için ayrı script mi yüklemeliyim?
**C:** Hayır! Aynı script tüm hisselerde çalışır. Sadece her hisse için ayrı alert kurarsınız.

### S: Alert limiti var mı?
**C:** TradingView'da plan bazlı alert limitleri var:
- Free: 1 aktif alert
- Pro: 20 aktif alert
- Pro+: 100 aktif alert
- Premium: 400 aktif alert

### S: Telegram mesajları hala gelir mi?
**C:** Evet! Her hisse için aldığınız alert Telegram'a mesaj gönderir (anyalert ile).

---

## 📊 Diğer Modüllerle Karşılaştırma

| Özellik | EMA Cross | SuperDip | Pullback | E2 |
|---------|-----------|----------|----------|-----|
| **Çalışma Şekli** | Mevcut grafik | Mevcut grafik | Mevcut grafik | Mevcut grafik |
| **Watchlist Tarama** | ❌ Yok | ❌ Yok | ❌ Yok | ❌ Yok |
| **Alert Sistemi** | ✅ TradingView | ✅ TradingView | ✅ TradingView | ✅ TradingView |
| **Telegram Entegrasyonu** | ✅ Var | ✅ Var | ✅ Var | ✅ Var |
| **Request.security Kullanımı** | 3 çağrı | ~5 çağrı | ~3 çağrı | ~5 çağrı |

**Sonuç:** Tüm modüller aynı şekilde çalışır. Tutarlı ve standart yapı.

---

## ✅ Avantajlar

### 1. Basitlik
- Kod çok daha basit ve anlaşılır
- Karmaşık watchlist parsing yok
- Bakımı kolay

### 2. Request.security Limiti Çözüldü
- Önceden: 120+ request.security çağrısı (40 sembol × 3)
- Şimdi: 3 request.security çağrısı (sadece mevcut hisse)
- Limit sorunu tamamen ortadan kalktı

### 3. TradingView Standartlarına Uyum
- Diğer göstergeler gibi çalışır
- TradingView'un alert sistemi ile uyumlu
- Kullanıcılar için tanıdık

### 4. Esneklik
- Kullanıcı istediği hisseyi izleyebilir
- Alert sayısını planına göre ayarlayabilir
- Chat ID'leri hisse bazlı ayarlayabilir

---

## 🎉 Sonuç

**EMA modülü artık diğer modüller gibi çalışıyor:**
- ✅ Sadece açık grafikteki hisse için sinyal
- ✅ TradingView alert sistemi ile uyumlu
- ✅ Request.security limiti sorunu yok
- ✅ Basit ve anlaşılır kod
- ✅ Telegram entegrasyonu çalışıyor
- ✅ SuperDip, Pullback, E2 ile aynı yapı

**Kullanım:** Her izlemek istediğiniz hisse için TradingView'da ayrı alert kurun!

---

**Durum:** ✅ Tamamlandı
**Tarih:** 07.02.2026
**Versiyon:** v7.1 (Watchlist kaldırıldı)
