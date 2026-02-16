# ✅ EMA Mesaj Formatı Güncellendi

## 📝 Yapılan Değişiklikler

### 1. Chat ID'ler (Değişmedi - Zaten Var)

**AL (BUY) Mesajları:**
- Chat ID: `ema_buy_chat_id` (Satır 149)
- Varsayılan: `-1002781417418`
- Kullanım: Satır 1876

**SAT (SELL) Mesajları:**
- Chat ID: `ema_sell_chat_id` (Satır 150)
- Varsayılan: `-1002587291984`
- Kullanım: Satır 1884

✅ **AL ve SAT mesajları farklı Telegram gruplarına gidiyor!**

---

### 2. Mesaj Formatı (Güncellendi)

#### Önceki Format (İngilizce)
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

#### Yeni Format (Türkçe)
```
⚡ EMA KESİŞME 15 Dakika ve 1 Saat • AL
HISSE: THYAO | FIYAT: 315.50

TETİK: 1 Saat EMA5 yukarı kesti EMA137
ONAY: 15 Dakika EMA5 > EMA137

1 Saat EMA5: 315.50
1 Saat EMA137: 310.00
15 Dakika EMA5: 316.00
15 Dakika EMA137: 311.00
```

#### SAT Mesajı (Yeni Format)
```
⚡ EMA KESİŞME 15 Dakika ve 1 Saat • SAT
HISSE: THYAO | FIYAT: 308.00

TETİK: 1 Saat EMA5 aşağı kesti EMA137
ONAY: 15 Dakika EMA5 < EMA137

1 Saat EMA5: 308.00
1 Saat EMA137: 310.00
15 Dakika EMA5: 307.50
15 Dakika EMA137: 309.00
```

---

## 📊 Değişiklik Detayları

### Başlık
- ❌ **Eski:** `"⚡ EMA CROSS 1H • BUY (AL)"`
- ✅ **Yeni:** `"⚡ EMA KESİŞME 15 Dakika ve 1 Saat • AL"`

### Sinyal Tipi
- ❌ **Eski:** `"BUY (AL)"` / `"SELL (SAT)"`
- ✅ **Yeni:** `"AL"` / `"SAT"`

### Zaman Dilimleri
- ❌ **Eski:** `"1H"` / `"15m"`
- ✅ **Yeni:** `"1 Saat"` / `"15 Dakika"`

### Onay Mesajı
- ❌ **Eski:** `"ONAY: 15m EMA5 > EMA137 (STATE)"`
- ✅ **Yeni:** `"ONAY: 15 Dakika EMA5 > EMA137"`

---

## 🎯 Özellikler

### ✅ Hisse Adı
- `syminfo.ticker` ile otomatik
- Örnek: THYAO, PETKM, SASA

### ✅ Fiyat
- `close` değeri
- `fmtMintMsg()` fonksiyonu ile formatlanmış
- Örnek: 315.50, 308.25

### ✅ 15 Dakika ve 1 Saat Bilgisi
- Başlıkta: "EMA KESİŞME 15 Dakika ve 1 Saat"
- Tetik: "1 Saat EMA5..."
- Onay: "15 Dakika EMA5..."
- Detaylar: Her iki zaman dilimi için EMA değerleri

### ✅ Farklı Chat ID'ler
- AL → `ema_buy_chat_id`
- SAT → `ema_sell_chat_id`

---

## 📱 Telegram'a Nasıl Gider?

### AL Sinyali Geldiğinde:
1. EMA5, 1 saatlik grafik (60 dakika) üzerinde EMA137'yi yukarı keser
2. 15 dakikalık grafik üzerinde EMA5 > EMA137 (state confirmation)
3. Mesaj `ema_buy_chat_id` chat'ine gönderilir
4. Format: "⚡ EMA KESİŞME 15 Dakika ve 1 Saat • AL"

### SAT Sinyali Geldiğinde:
1. EMA5, 1 saatlik grafik üzerinde EMA137'yi aşağı keser
2. 15 dakikalık grafik üzerinde EMA5 < EMA137 (state confirmation)
3. Mesaj `ema_sell_chat_id` chat'ine gönderilir
4. Format: "⚡ EMA KESİŞME 15 Dakika ve 1 Saat • SAT"

---

## 🔧 Kod Değişiklikleri

### Dosya: `Pullbackformasyon ve dip_v7.txt`

**Satır 149-150:** Chat ID Input'ları (Değişmedi)
```pinescript
ema_buy_chat_id=input.string("-1002781417418","EMA BUY chat_id",group=grpEMA)
ema_sell_chat_id=input.string("-1002587291984","EMA SELL chat_id",group=grpEMA)
```

**Satır 1858-1872:** Mesaj Fonksiyonu (Güncellendi)
```pinescript
f_ema_build_msg(isBuy) =>
    lines = array.new_string()
    signalType = isBuy ? "AL" : "SAT"
    array.push(lines, "⚡ EMA KESİŞME 15 Dakika ve 1 Saat • " + signalType)
    array.push(lines, "HISSE: " + syminfo.ticker + " | FIYAT: " + fmtMintMsg(close))
    array.push(lines, "")
    array.push(lines, "TETİK: 1 Saat EMA" + str.tostring(ema_fast) + " " + (isBuy ? "yukarı kesti" : "aşağı kesti") + " EMA" + str.tostring(ema_slow))
    array.push(lines, "ONAY: 15 Dakika EMA" + str.tostring(ema_fast) + " " + (isBuy ? ">" : "<") + " EMA" + str.tostring(ema_slow))
    array.push(lines, "")
    array.push(lines, "1 Saat EMA" + str.tostring(ema_fast) + ": " + fmtMintMsg(ema1h_fast))
    array.push(lines, "1 Saat EMA" + str.tostring(ema_slow) + ": " + fmtMintMsg(ema1h_slow))
    array.push(lines, "15 Dakika EMA" + str.tostring(ema_fast) + ": " + fmtMintMsg(ema15m_fast))
    array.push(lines, "15 Dakika EMA" + str.tostring(ema_slow) + ": " + fmtMintMsg(ema15m_slow))
    f_lineJoin(lines)
```

**Satır 1875-1889:** Mesaj Gönderme (Değişmedi)
```pinescript
if ema_buy_signal
    send_msg(ema_buy_chat_id, f_ema_build_msg(true))
    ...

if ema_sell_signal
    send_msg(ema_sell_chat_id, f_ema_build_msg(false))
    ...
```

---

## ✅ Kontrol Listesi

- [x] Chat ID'ler var mı? **✅ Evet** (Satır 149-150)
- [x] AL ve SAT farklı chat'e gidiyor mu? **✅ Evet** (Satır 1876, 1884)
- [x] Mesajda "EMA KESİŞME 15 Dakika ve 1 Saat" var mı? **✅ Evet**
- [x] Hisse adı var mı? **✅ Evet** (`syminfo.ticker`)
- [x] Fiyat var mı? **✅ Evet** (`close` değeri)
- [x] Zaman dilimleri Türkçe mi? **✅ Evet** (1 Saat, 15 Dakika)

---

## 🎉 Sonuç

✅ **AL ve SAT mesajları farklı Telegram gruplarına gidiyor**
✅ **Mesaj formatı Türkçe ve açıklayıcı**
✅ **15 Dakika ve 1 Saat bilgisi açıkça belirtilmiş**
✅ **Hisse adı ve fiyat her mesajda var**

---

**Durum:** ✅ Tamamlandı
**Tarih:** 07.02.2026
**Versiyon:** v7.2 (Mesaj formatı Türkçeleştirildi)
