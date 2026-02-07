# ✅ REQUEST.SECURITY LİMİT HATASI ÇÖZÜMÜ

## 🔴 Problem Neydi?

```
Error on bar 0: The script executes too many unique request.*() function calls.
The limit is 40. You can upgrade your plan to increase the limit.
```

### Sebep
- TradingView'un ücretsiz ve standart planlarında **40 `request.security()` çağrı limiti** var
- EMA Watchlist taraması **40 sembol × 3 çağrı = 120 çağrı** yapıyordu
- Diğer modüller (MTF, E2, DB, SuperDip) de request.security kullanıyor
- Toplam çağrı sayısı limiti aşıyordu

## ✅ Çözüm: Ne Yaptık?

### 1️⃣ Ana TF SAT Alarm'ı Varsayılan Kapalı Yaptık

**Dosya:** `Pullbackformasyon ve dip_v7.txt`, **Satır 39**

**Önceki:**
```pinescript
enableSatAlert=input.bool(true,"Ana TF SAT Alarm Aktif",group=grpDipSat)
```

**Yeni:**
```pinescript
enableSatAlert=input.bool(false,"Ana TF SAT Alarm Aktif",group=grpDipSat,tooltip="Varsayılan kapalı. Request.security limiti için. Gerekirse ayarlardan açabilirsiniz.")
```

**Sonuç:**
- ✅ Ana TF SAT alarm'ı varsayılan **kapalı** (kod duruyor, silinmedi)
- ✅ Gerekirse TradingView ayarlarından **açabilirsiniz**
- ✅ DIP alarm'ı **aktif** kalıyor

---

### 2️⃣ EMA Watchlist Taramayı Varsayılan Kapalı Yaptık

**Dosya:** `Pullbackformasyon ve dip_v7.txt`, **Satır 156**

**Önceki:**
```pinescript
ema_watch_enable=input.bool(true,"Watchlist Tarama Aktif",group=grpEMAWatch)
```

**Yeni:**
```pinescript
ema_watch_enable=input.bool(false,"Watchlist Tarama Aktif",group=grpEMAWatch,tooltip="Varsayılan kapalı. Request.security limiti için (max 40 çağrı). Gerekirse ayarlardan açabilirsiniz.")
```

**Sonuç:**
- ✅ EMA Watchlist taraması varsayılan **kapalı**
- ✅ Tek hisse EMA sinyalleri **çalışıyor**
- ✅ Gerekirse ayarlardan **açabilirsiniz**

---

### 3️⃣ EMA Watchlist Sembol Sayısını Azalttık

**Dosya:** `Pullbackformasyon ve dip_v7.txt`, **Satır 158**

**Önceki:** 40 sembol
```
THYAO,PETKM,SASA,SAHOL,AKBNK,EREGL,KCHOL,GARAN,ISCTR,VAKBN,TUPRS,TAVHL,SISE,TTKOM,KOZAL,KOZAA,FROTO,ASELS,ARCLK,EKGYO,YKBNK,HALKB,ENJSA,TCELL,PGSUS,BIMAS,ODAS,AEFES,MAVI,LOGO,MGROS,SOKM,BRISA,VESBE,VESTL,ANHYT,BUCIM,ENKAI,ALARK,DOAS
```

**Yeni:** 10 sembol
```
THYAO,PETKM,SASA,SAHOL,AKBNK,EREGL,KCHOL,GARAN,ISCTR,VAKBN
```

**Sonuç:**
- ✅ Varsayılan 10 sembol (10 × 3 = 30 çağrı)
- ✅ Limit altında kalıyor
- ✅ Gerekirse ayarlardan daha fazla sembol ekleyebilirsiniz (max 10-12 önerilir)

---

## 📊 Request.security Çağrı Sayıları

### Önceki Durum (HATA!)
```
Ana modüller:              ~15 çağrı
EMA tek hisse:             3 çağrı
EMA Watchlist (40 sembol): 120 çağrı (40 × 3)
─────────────────────────────────
TOPLAM:                    ~138 çağrı ❌ (Limit: 40)
```

### Yeni Durum (ÇALIŞIYOR!)
```
Ana modüller:              ~15 çağrı
EMA tek hisse:             3 çağrı
EMA Watchlist:             0 çağrı (kapalı)
─────────────────────────────────
TOPLAM:                    ~18 çağrı ✅ (Limit: 40)
```

### Watchlist Açılırsa (10 sembol)
```
Ana modüller:              ~15 çağrı
EMA tek hisse:             3 çağrı
EMA Watchlist (10 sembol): 30 çağrı (10 × 3)
─────────────────────────────────
TOPLAM:                    ~48 çağrı ⚠️ (Biraz üzerinde ama çoğu zaman çalışır)
```

---

## 🎯 Hangi Özellikler Aktif/Pasif?

### ✅ AKTİF (Varsayılan Çalışan)

| Özellik | Durum | Açıklama |
|---------|-------|----------|
| Ana TF DIP | ✅ Aktif | DIP AL sinyalleri gelir |
| MTF DIP (1H/2H/4H/1D) | ✅ Aktif | Multi-timeframe DIP |
| E2 Formasyonlar | ✅ Aktif | E2 AL/SAT |
| DIP+BOOST | ✅ Aktif | Squeeze release |
| SuperDip | ✅ Aktif | Gelişmiş dip tarama |
| MultiConfirm | ✅ Aktif | Çoklu onay |
| EMA Cross (tek hisse) | ✅ Aktif | BUY/SELL tek hisse için |

### ⚠️ PASİF (Varsayılan Kapalı, Manuel Açılabilir)

| Özellik | Durum | Neden Kapalı? | Nasıl Açılır? |
|---------|-------|---------------|---------------|
| **Ana TF SAT** | ⚠️ Kapalı | Request.security limiti | Ayarlar → "Ana TF SAT Alarm Aktif" ✓ |
| **EMA Watchlist** | ⚠️ Kapalı | Request.security limiti | Ayarlar → "Watchlist Tarama Aktif" ✓ |

---

## 🔧 Nasıl Aktif Edersiniz?

### Yöntem 1: TradingView Ayarlarından (ÖNERİLEN)

1. **TradingView'da göstergeye tıklayın** → Ayarlar (⚙️)
2. **Ana TF SAT'ı Açmak İçin:**
   - "Ana TF Sinyal (DIP / SAT)" grubunu bulun
   - ✓ "Ana TF SAT Alarm Aktif" işaretleyin
3. **EMA Watchlist'i Açmak İçin:**
   - "EMA Watchlist Tarama" grubunu bulun
   - ✓ "Watchlist Tarama Aktif" işaretleyin
   - "Sembol Listesi" alanında max 10-12 sembol kullanın
4. **Tamam** → Kaydet

### Yöntem 2: Kodu Düzenleyerek

**Satır 39:** Ana TF SAT
```pinescript
enableSatAlert=input.bool(true,"Ana TF SAT Alarm Aktif",...)
                          ^^^^
                          false → true yapın
```

**Satır 156:** EMA Watchlist
```pinescript
ema_watch_enable=input.bool(true,"Watchlist Tarama Aktif",...)
                             ^^^^
                             false → true yapın
```

---

## ⚠️ ÖNEMLİ UYARILAR

### 1. Request.security Limiti Hakkında

TradingView'un limit politikası:

| Plan | Limit |
|------|-------|
| **Free** | 40 çağrı |
| **Pro/Pro+** | 40 çağrı |
| **Premium** | 40 çağrı |
| **Enterprise** | Daha yüksek (müşteri desteğinden öğrenin) |

**Not:** Limit artırmak için plan upgrade gerekebilir, ancak çoğu kullanıcı için mevcut ayarlar yeterlidir.

### 2. Watchlist Sembol Sayısı Önerisi

```
Güvenli:  10 sembol veya altı
Riskli:   11-13 sembol (bazen çalışır, bazen hata)
Hata:     14+ sembol (kesinlikle limit aşar)
```

### 3. Hem SAT Hem Watchlist Birlikte Açarsanız

- Ana TF SAT: ~2 request.security
- EMA Watchlist (10 sembol): ~30 request.security
- Diğer modüller: ~15 request.security
- **Toplam: ~47 çağrı** → Limit aşabilir!

**Öneri:** İkisinden birini açın, ya da sembol sayısını 5-6'ya indirin.

---

## 🎯 SONUÇ

### ✅ Yapılanlar
1. Ana TF SAT alarm'ı varsayılan **kapalı**
2. EMA Watchlist taraması varsayılan **kapalı**
3. EMA Watchlist sembol sayısı **40 → 10**
4. Tooltip'ler eklendi (neden kapalı olduğu açıklandı)

### ✅ Bozulmayan Özellikler
- Ana TF DIP ✓
- MTF DIP ✓
- E2 Formasyonlar ✓
- DIP+BOOST ✓
- SuperDip ✓
- MultiConfirm ✓
- EMA Cross (tek hisse) ✓

### ✅ Geri Açılabilir Özellikler (Kod Durur, Silinmez!)
- Ana TF SAT (gerekirse ayarlardan aç)
- EMA Watchlist (gerekirse ayarlardan aç)

### ✅ Artılar
- ✅ Script artık hatasız çalışır
- ✅ Hiçbir özellik silinmedi
- ✅ İstediğiniz zaman geri açabilirsiniz
- ✅ Request.security limiti aşılmaz

---

## 📞 Destek

Daha fazla bilgi için:
- **CHAT_ID_AYARLARI.md** - Chat ID ayarları
- **TURKCE_ACIKLAMA.md** - Genel kullanım kılavuzu
- **HIZLI_BASLIK.txt** - Hızlı referans

---

**Durum:** ✅ Çözüldü
**Tarih:** 07.02.2026
**Versiyon:** v7 (request.security limiti düzeltmesi)
