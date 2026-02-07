# EMA Cross Modülü - Türkçe Kullanım Kılavuzu

## ⚠️ ÖNEMLİ: KOD ZATEN EKLENDİ!

Kafanız karışmasın - **hiçbir şey manuel olarak eklemeniz gerekmiyor!**

Ben zaten tüm değişiklikleri `Pullbackformasyon ve dip_v7.txt` dosyasına ekledim.

## 📊 Ne Yapıldı?

### Önceki Durum
```
Pullbackformasyon ve dip_v7.txt: 3,157 satır
```

### Şimdiki Durum
```
Pullbackformasyon ve dip_v7.txt: 3,360 satır (+203 satır)
```

### Eklenen Kod Nerede?

**1. Input Ayarları (Satır 142-163)**
```pinescript
// ===================== EMA CROSS MODULE (1H + 15m Confirm) =====================
grpEMA="EMA Cross (1H + 15m Onay)"
ema_enable=input.bool(true,"EMA Cross Modülü Aktif",group=grpEMA)
ema_fast=input.int(5,"EMA Fast (Hızlı)",minval=1,group=grpEMA)
ema_slow=input.int(137,"EMA Slow (Yavaş)",minval=1,group=grpEMA)
// ... diğer ayarlar
```

**2. Ana Mantık Kodu (Satır 1823-2004)**
```pinescript
// ===================== 3.5) EMA CROSS MODULE (1H + 15m Confirm) =======
// EMA hesaplamaları, sinyal üretme, mesaj gönderme vs.
```

## ✅ Yapmanız Gerekenler (Sadece 3 Adım!)

### Adım 1: Dosyayı TradingView'a Yükleyin

1. TradingView'u açın
2. Pine Editor'ı açın (Alt+E)
3. `Pullbackformasyon ve dip_v7.txt` dosyasının **TÜM İÇERİĞİNİ** kopyalayın
4. Pine Editor'a yapıştırın
5. "Kaydet" butonuna basın
6. "Grafiğe Ekle" butonuna basın

### Adım 2: Derlemeyi Kontrol Edin

✅ Script hatasız yüklenmeli
✅ Grafik üzerinde "MGPULL+ Formasyon +" göstergesi görünmeli

### Adım 3: Ayarları Kontrol Edin

1. Gösterge adına tıklayın → "Ayarlar" (⚙️)
2. Aşağı kaydırın ve şu grupları bulun:
   - **"EMA Cross (1H + 15m Onay)"** ✓
   - **"EMA Watchlist Tarama"** ✓
3. Varsayılan değerleri kontrol edin:
   - ✓ EMA Cross Modülü Aktif
   - ✓ EMA Fast = 5
   - ✓ EMA Slow = 137
   - ✓ BUY Sinyalleri Aktif
   - ✗ SELL Sinyalleri Aktif (kapalı - güvenli)

## 📁 Dosya Yapısı

```
Pullbackformasyon ve dip_v7.txt (3,360 satır)
│
├─ Satır 1-141: Eski input ayarları
├─ Satır 142-163: ✨ YENİ: EMA Cross input ayarları
├─ Satır 164-1822: Eski kod (helper fonksiyonlar, ana mantık)
├─ Satır 1823-2004: ✨ YENİ: EMA Cross ana mantığı
└─ Satır 2005-3360: Eski kod devamı (SuperDip vs.)
```

## ❌ YAPMAMANIZ GEREKENLER

❌ Kodu dosyanın sonuna eklemeyin
❌ 220 satırlık kodu ayrı bir dosyaya kaydetmeyin
❌ Manuel olarak hiçbir şey eklemeyin
❌ Dosyayı değiştirmeyin

## ✅ DOĞRU: Kod Zaten Entegre Edildi!

Ben kodu **doğru yerlere** ekledim:
- Input ayarları → Diğer input'ların yanına
- Ana mantık → DIP+BOOST modülünden sonra, SuperDip'ten önce

## 🎯 Test Etmek İçin

1. Grafiği 1H zaman dilimine ayarlayın
2. BIST:THYAO gibi bir hisse seçin
3. Yeşil "EMA BUY" etiketlerini arayın
4. Kırmızı "EMA SELL" etiketi olmamalı (devre dışı)

## 📱 Telegram Mesajı Örneği

Script çalıştığında şöyle mesajlar alacaksınız:

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

## ⚙️ Watchlist Tarama

Watchlist kullanmak isterseniz:

1. Ayarlar → "EMA Watchlist Tarama"
2. ✓ "Watchlist Tarama Aktif" işaretli olmalı
3. "Sembol Listesi" alanını düzenleyin:
   ```
   THYAO,PETKM,SASA,AKBNK,EREGL
   ```
4. Her 1H kapanışında toplu mesaj alırsınız:
   ```
   ⚡ EMA CROSS 1H TARAMA • BUY (AL)
   
   HISSELER (3):
   • THYAO
   • PETKM
   • SASA
   ```

## 🔧 Ayarları Değiştirmek

### SELL Sinyallerini Aktif Etmek
Ayarlar → "EMA Cross" → ✓ "SELL Sinyalleri Aktif"

### EMA Periyotlarını Değiştirmek
Ayarlar → "EMA Cross" → "EMA Fast" ve "EMA Slow" değerlerini değiştirin

### Cooldown Süresini Artırmak
Ayarlar → "EMA Cross" → "EMA Cooldown (dk)" → 120 veya 180 yapın

## 📚 Ek Dökümantasyon

Eğer detaylı bilgi isterseniz:
- **QUICK_START.md** - Hızlı başlangıç kılavuzu (İngilizce)
- **EMA_CROSS_MODULE_README.md** - Tam dokümantasyon
- **EMA_CROSS_TESTING_GUIDE.md** - Test senaryoları

## ❓ Sık Sorulan Sorular

**S: 220 satırlık kodu nereye ekleyeceğim?**
C: Hiçbir yere! Kod zaten dosyanın içinde.

**S: Dosyanın sonuna mı eklemeliyim?**
C: Hayır! Kod zaten doğru yerlere eklenmiş durumda.

**S: Manuel olarak bir şey yapmam gerekiyor mu?**
C: Hayır! Sadece dosyayı TradingView'a yükleyin.

**S: Eski alertlerim çalışmaya devam eder mi?**
C: Evet! Tüm eski alertler aynen çalışır. Hiçbir değişiklik yok.

**S: SELL sinyalleri neden gelmiyor?**
C: Güvenlik için varsayılan olarak kapalı. Açmak isterseniz ayarlardan aktif edin.

**S: Watchlist çalışmıyor?**
C: Grafiğin 1H (veya daha yüksek) zaman diliminde olduğundan emin olun.

## 🎉 Özet

1. ✅ Kod zaten ekli - `Pullbackformasyon ve dip_v7.txt` dosyası hazır
2. ✅ Sadece TradingView'a yükleyin
3. ✅ Hiçbir manuel işlem gerekmez
4. ✅ Test edin ve kullanmaya başlayın!

---

**Tarih:** 07.02.2026
**Durum:** ✅ Hazır ve Kullanıma Uygun
**Gerekli İşlem:** Sadece TradingView'a yükleyin!
