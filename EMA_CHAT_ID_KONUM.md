# 📍 EMA5 Kesişme Telegram Chat ID Konumu

## ✅ Buldum! İşte Satırlar:

### 📱 Chat ID'ler Nerede?

**Dosya:** `Pullbackformasyon ve dip_v7.txt`

---

## 🎯 SATIR 149: EMA AL (BUY) Chat ID

```pinescript
ema_buy_chat_id=input.string("-1002781417418","EMA BUY chat_id",group=grpEMA)
```

**Ne İşe Yarar:**
- EMA5 yukarı kesişme (AL sinyali) geldiğinde
- Bu chat ID'ye Telegram mesajı gönderilir
- Varsayılan: `-1002781417418`

---

## 🎯 SATIR 150: EMA SAT (SELL) Chat ID

```pinescript
ema_sell_chat_id=input.string("-1002587291984","EMA SELL chat_id",group=grpEMA)
```

**Ne İşe Yarar:**
- EMA5 aşağı kesişme (SAT sinyali) geldiğinde
- Bu chat ID'ye Telegram mesajı gönderilir
- Varsayılan: `-1002587291984`

---

## 📋 Tam Bölüm (Satır 143-153)

```pinescript
143. grpEMA="EMA Cross (1H + 15m Onay)"
144. ema_enable=input.bool(true,"EMA Cross Modülü Aktif",group=grpEMA)
145. ema_fast=input.int(5,"EMA Fast (Hızlı)",minval=1,group=grpEMA)
146. ema_slow=input.int(137,"EMA Slow (Yavaş)",minval=1,group=grpEMA)
147. ema_enable_buy=input.bool(true,"BUY Sinyalleri Aktif",group=grpEMA)
148. ema_enable_sell=input.bool(false,"SELL Sinyalleri Aktif",group=grpEMA)
149. ema_buy_chat_id=input.string("-1002781417418","EMA BUY chat_id",group=grpEMA)   ⬅️ AL CHAT ID
150. ema_sell_chat_id=input.string("-1002587291984","EMA SELL chat_id",group=grpEMA)  ⬅️ SAT CHAT ID
151. ema_cooldown_min=input.int(60,"EMA Cooldown (dk)",minval=0,group=grpEMA)
152. ema_show_labels=input.bool(true,"EMA Label Göster",group=grpEMA)
```

---

## 🔧 Nasıl Değiştirirsiniz?

### Yöntem 1: Kodu Düzenleyerek
1. Dosyayı açın: `Pullbackformasyon ve dip_v7.txt`
2. **Satır 149**'a gidin → AL için chat ID'yi değiştirin
3. **Satır 150**'ye gidin → SAT için chat ID'yi değiştirin
4. Kaydedin ve TradingView'a yükleyin

### Yöntem 2: TradingView Ayarlarından (ÖNERİLEN)
1. Script'i TradingView'a yükleyin
2. Gösterge → **Ayarlar** (⚙️)
3. **"EMA Cross (1H + 15m Onay)"** grubunu bulun
4. **"EMA BUY chat_id"** → Kendi AL chat ID'nizi girin
5. **"EMA SELL chat_id"** → Kendi SAT chat ID'nizi girin
6. **Tamam** → Kaydet

---

## 📊 Chat ID'ler Nasıl Kullanılıyor?

### Satır 1876: AL Mesajı Gönderiliyor
```pinescript
if ema_buy_signal
    send_msg(ema_buy_chat_id, f_ema_build_msg(true))
    ema_lastBuyTime := time
```
**Sonuç:** AL sinyali geldiğinde → `ema_buy_chat_id` chat'ine mesaj gider

### Satır 1884: SAT Mesajı Gönderiliyor
```pinescript
if ema_sell_signal
    send_msg(ema_sell_chat_id, f_ema_build_msg(false))
    ema_lastSellTime := time
```
**Sonuç:** SAT sinyali geldiğinde → `ema_sell_chat_id` chat'ine mesaj gider

---

## 💡 Örnek Chat ID'ler

### Senaryo 1: Farklı Gruplar (Önerilen)
```pinescript
ema_buy_chat_id="-1234567890"   // AL sinyalleri buraya
ema_sell_chat_id="-9876543210"  // SAT sinyalleri buraya
```

### Senaryo 2: Aynı Grup
```pinescript
ema_buy_chat_id="-1111111111"   // Her ikisi de
ema_sell_chat_id="-1111111111"  // aynı gruba
```

---

## ✅ Özet

| Ne? | Satır | Varsayılan | Açıklama |
|-----|-------|------------|----------|
| **AL Chat ID** | 149 | -1002781417418 | EMA yukarı kesişme mesajları |
| **SAT Chat ID** | 150 | -1002587291984 | EMA aşağı kesişme mesajları |

---

## 🎯 Hızlı Bul

**Komut ile bulmak için:**
```bash
grep -n "ema.*chat_id" "Pullbackformasyon ve dip_v7.txt"
```

**Çıktı:**
```
149:ema_buy_chat_id=input.string("-1002781417418","EMA BUY chat_id",group=grpEMA)
150:ema_sell_chat_id=input.string("-1002587291984","EMA SELL chat_id",group=grpEMA)
1876:    send_msg(ema_buy_chat_id, f_ema_build_msg(true))
1884:    send_msg(ema_sell_chat_id, f_ema_build_msg(false))
```

---

**Durum:** ✅ Bulundu!
**Tarih:** 08.02.2026
