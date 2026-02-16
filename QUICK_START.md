# EMA Cross Module - Quick Start Guide

## 🎯 What Was Added

A new **EMA Cross module** that sends Telegram alerts when:
- 1H EMA5 crosses EMA137 (up for BUY, down for SELL)
- 15m EMA5 is above/below EMA137 (state confirmation)
- Scans multiple symbols (watchlist) on 1H bar close

## 🚀 How to Use

### Step 1: Load Script
1. Open TradingView
2. Press `Alt+E` to open Pine Editor
3. Copy all contents from `Pullbackformasyon ve dip_v7.txt`
4. Paste into editor
5. Click "Save" then "Add to Chart"

### Step 2: Verify Compilation
✅ Script should load without errors  
✅ Check for "MGPULL+ Formasyon +" in chart legend  

### Step 3: Configure Settings
1. Click indicator name → Settings (⚙️)
2. Scroll to **"EMA Cross (1H + 15m Onay)"** group
3. Verify defaults:
   - ✓ EMA Cross Modülü Aktif
   - ✓ EMA Fast = 5
   - ✓ EMA Slow = 137
   - ✓ BUY Sinyalleri Aktif
   - ✗ SELL Sinyalleri Aktif (disabled - safe default)

### Step 4: Test on Chart
1. Set chart to **1H timeframe**
2. Use any Turkish stock (e.g., BIST:THYAO)
3. Look for green "EMA BUY" labels
4. No red "EMA SELL" labels (disabled by default)

### Step 5: Enable Watchlist (Optional)
1. Settings → **"EMA Watchlist Tarama"** group
2. Ensure ✓ "Watchlist Tarama Aktif"
3. Edit symbol list (comma-separated):
   ```
   THYAO,PETKM,SASA,AKBNK,EREGL
   ```
4. On next 1H close, receive aggregated message

## 📱 Message Examples

### Single Symbol BUY
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

### Watchlist Scan (Aggregated)
```
⚡ EMA CROSS 1H TARAMA • BUY (AL)

TETİK: 1H EMA5 yukarı kesti EMA137
ONAY: 15m EMA5 > EMA137 (STATE)

HISSELER (3):
• THYAO
• PETKM
• SASA
```

## ⚙️ Key Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `ema_enable` | ✓ | Master switch |
| `ema_fast` | 5 | Fast EMA period |
| `ema_slow` | 137 | Slow EMA period |
| `ema_enable_buy` | ✓ | Enable BUY alerts |
| `ema_enable_sell` | ✗ | Enable SELL alerts |
| `ema_cooldown_min` | 60 | Minutes between alerts |
| `ema_watch_enable` | ✓ | Enable watchlist scan |
| `ema_watch_prefix` | BIST: | Symbol prefix |

## 🔧 Common Adjustments

### Enable SELL Alerts
Settings → "EMA Cross" → Check ✓ "SELL Sinyalleri Aktif"

### Change EMA Periods
Settings → "EMA Cross" → Adjust "EMA Fast" and "EMA Slow"

### Reduce Alert Frequency
Settings → "EMA Cross" → Increase "EMA Cooldown (dk)" to 120 or 180

### Custom Symbol List
Settings → "EMA Watchlist Tarama" → Edit "Sembol Listesi"
```
Example: THYAO,PETKM,SASA,AKBNK,EREGL,KCHOL
```

### Separate Chat IDs
Settings → "EMA Cross" → Enter different values for:
- "EMA BUY chat_id"
- "EMA SELL chat_id"

## 🎓 Full Documentation

- **Features:** `EMA_CROSS_MODULE_README.md`
- **Testing:** `EMA_CROSS_TESTING_GUIDE.md`
- **Technical:** `IMPLEMENTATION_SUMMARY.md`

## ❓ FAQ

**Q: Why no SELL alerts?**  
A: SELL is disabled by default. Enable in settings if needed.

**Q: Watchlist not working?**  
A: Ensure chart is on 1H (or higher) timeframe and "Watchlist Tarama Aktif" is checked.

**Q: Too many alerts?**  
A: Increase cooldown (60 → 120 min) or reduce symbol count.

**Q: Wrong exchange?**  
A: Change "Sembol Prefix" from "BIST:" to your exchange (e.g., "NASDAQ:")

## ✅ Success Checklist

- [ ] Script loaded without errors
- [ ] Settings visible in indicator configuration
- [ ] BUY signals fire on 1H cross + 15m confirm
- [ ] SELL disabled by default (no alerts)
- [ ] Watchlist scan sends aggregated messages
- [ ] Cooldown prevents spam
- [ ] Existing alerts (DIP, SAT, MTF, etc.) still work

## 🆘 Need Help?

1. Check **IMPLEMENTATION_SUMMARY.md** for architecture
2. Review **EMA_CROSS_TESTING_GUIDE.md** for test scenarios
3. See **EMA_CROSS_MODULE_README.md** for detailed specs

---

**Implementation Date:** 2026-02-07  
**Status:** ✅ Complete and Ready  
**Branch:** copilot/add-ema-cross-module
