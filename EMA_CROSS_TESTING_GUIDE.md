# EMA Cross Module - Testing Guide

## Quick Test Procedure

### 1. Load Script on TradingView
1. Open TradingView
2. Copy contents of `Pullbackformasyon ve dip_v7.txt`
3. Open Pine Editor (Alt+E or click "Pine Editor" at bottom)
4. Paste the script
5. Click "Save" → "Add to Chart"

### 2. Verify Compilation
✓ **Expected:** Script loads without errors
✓ **Check:** No red error messages in Pine Editor
✓ **Indicator name:** "MGPULL+ Formasyon +" appears in chart legend

### 3. Check Input Settings
1. Click on indicator name in chart legend → "Settings" (gear icon)
2. Scroll down to find new groups:
   - ✓ **"EMA Cross (1H + 15m Onay)"** group exists
   - ✓ **"EMA Watchlist Tarama"** group exists
3. Verify default values:
   - `EMA Cross Modülü Aktif` = ☑ (checked)
   - `EMA Fast (Hızlı)` = 5
   - `EMA Slow (Yavaş)` = 137
   - `BUY Sinyalleri Aktif` = ☑ (checked)
   - `SELL Sinyalleri Aktif` = ☐ (unchecked) ← **Important!**
   - `EMA Cooldown (dk)` = 60
   - `Watchlist Tarama Aktif` = ☑ (checked)

### 4. Visual Verification
1. Change chart to 1H timeframe
2. Look for EMA labels on chart:
   - Green "EMA BUY" labels (pointing up)
   - No red "EMA SELL" labels (disabled by default)

### 5. Alert Verification
1. Click "Create Alert" (⏰ icon)
2. In "Condition" dropdown, find:
   - ✓ "EMA CROSS BUY (1H+15m)"
   - ✓ "EMA CROSS SELL (1H+15m)"
3. Verify existing alerts still present:
   - ✓ "DIP AL Sinyali (AnaTF)"
   - ✓ "YÜKSELDİ SAT Sinyali (AnaTF)"
   - ✓ "MTF 1H DIP", "MTF 2H DIP", etc.
   - ✓ "E2: AL (AnaTF)", "E2: SAT (AnaTF)"
   - ✓ "DIP+BOOST 4H WATCH", etc.

## Detailed Testing Scenarios

### Scenario 1: BUY Signal on Single Symbol

**Setup:**
- Chart: BIST:THYAO, 1H timeframe
- Settings: `ema_enable_buy = true`, `ema_enable_sell = false`

**Test Steps:**
1. Find a historical 1H bar where EMA5 crossed above EMA137
2. Check that at trigger time, 15m EMA5 was > EMA137
3. Verify label appears on chart
4. Check console/alert log for message

**Expected Result:**
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

### Scenario 2: SELL Signal Disabled (Default)

**Setup:**
- Same as Scenario 1
- Settings: `ema_enable_sell = false` (default)

**Test Steps:**
1. Find a historical 1H bar where EMA5 crossed below EMA137
2. Verify NO label appears
3. Verify NO message sent

**Expected Result:**
- ✓ No SELL label on chart
- ✓ No SELL message in alerts
- ✓ BUY signals still work

### Scenario 3: SELL Signal Enabled

**Setup:**
- Chart: BIST:THYAO, 1H timeframe
- Settings: `ema_enable_sell = true`

**Test Steps:**
1. Enable SELL in settings
2. Find a historical 1H bar where EMA5 crossed below EMA137
3. Check that at trigger time, 15m EMA5 was < EMA137
4. Verify red label appears on chart

**Expected Result:**
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

### Scenario 4: Cooldown Mechanism

**Setup:**
- Chart: BIST:THYAO, 1H timeframe
- Settings: `ema_cooldown_min = 60` (default)

**Test Steps:**
1. Note timestamp of first BUY signal
2. Look for another BUY signal within 60 minutes
3. Verify it's blocked by cooldown
4. Look for BUY signal after 60 minutes
5. Verify it triggers

**Expected Result:**
- ✓ First signal: Triggers normally
- ✓ Within cooldown: No alert (even if cross occurs)
- ✓ After cooldown: Triggers normally

### Scenario 5: Watchlist Scan - BUY Only

**Setup:**
- Chart: Any symbol, 1H timeframe
- Settings: 
  - `ema_watch_enable = true`
  - `ema_watch_prefix = "BIST:"`
  - `ema_watch_symbols = "THYAO,PETKM,SASA"`
  - `ema_enable_sell = false`

**Test Steps:**
1. Wait for 1H bar close (or replay historical data)
2. Check for aggregated message

**Expected Result (example with 2 matches):**
```
⚡ EMA CROSS 1H TARAMA • BUY (AL)

TETİK: 1H EMA5 yukarı kesti EMA137
ONAY: 15m EMA5 > EMA137 (STATE)

HISSELER (2):
• THYAO
• SASA
```

### Scenario 6: Watchlist Scan - BUY and SELL

**Setup:**
- Same as Scenario 5
- Settings: `ema_enable_sell = true`

**Test Steps:**
1. Wait for 1H bar close
2. Check for two messages (BUY and SELL)

**Expected Result:**
- ✓ BUY message with matching symbols
- ✓ SELL message with matching symbols
- ✓ Different chat_ids if configured

### Scenario 7: Empty Watchlist Scan

**Setup:**
- Same as Scenario 5
- No symbols match criteria

**Test Steps:**
1. Wait for 1H bar close
2. Verify no messages sent

**Expected Result:**
- ✓ No messages (list size = 0)
- ✓ No errors

### Scenario 8: Symbol List Parsing

**Setup:**
- Settings: `ema_watch_symbols = "THYAO, PETKM , SASA,AKBNK"` (spaces)

**Test Steps:**
1. Load script
2. Check parsed symbols

**Expected Result:**
- ✓ Spaces trimmed correctly
- ✓ Symbols: ["BIST:THYAO", "BIST:PETKM", "BIST:SASA", "BIST:AKBNK"]

### Scenario 9: Max 40 Symbols Enforcement

**Setup:**
- Settings: `ema_watch_symbols = "SYM1,SYM2,...,SYM50"` (50 symbols)

**Test Steps:**
1. Load script
2. Check number of symbols processed

**Expected Result:**
- ✓ Only first 40 symbols processed
- ✓ Remaining 10 ignored
- ✓ No errors

### Scenario 10: Existing Alerts Unchanged

**Setup:**
- Load updated script
- Configure chart with existing signals (DIP, SAT, MTF, etc.)

**Test Steps:**
1. Compare alerts before and after update
2. Verify all existing alertconditions still work

**Expected Result:**
- ✓ All 14 original alerts still present
- ✓ 2 new EMA alerts added (total = 16)
- ✓ No changes to existing alert behavior

## Common Issues and Solutions

### Issue: "Cannot call 'request.security' with too many symbols"
**Solution:** Reduce symbol count in `ema_watch_symbols` to ≤ 40

### Issue: SELL alerts not working
**Solution:** Check `ema_enable_sell = true` (it's disabled by default)

### Issue: Watchlist scan not triggering
**Solution:** 
- Verify chart is on 1H or higher timeframe
- Check `ema_watch_enable = true`
- Ensure at least one symbol in list

### Issue: Too many alerts
**Solution:** 
- Increase `ema_cooldown_min` (default: 60 minutes)
- Reduce symbol count in watchlist

### Issue: Wrong symbols in watchlist
**Solution:** Check `ema_watch_prefix` matches your exchange:
- Turkish stocks: "BIST:"
- Crypto: "BINANCE:", "COINBASE:", etc.
- US stocks: "NASDAQ:", "NYSE:", or "" (blank)

### Issue: Script compilation error
**Solution:** Ensure Pine Script v6 is supported. If not, the script may need v5 compatibility (contact support)

## Performance Monitoring

### request.security Call Count
- **Without watchlist:** 3 calls/bar (1H current, 1H prev, 15m current)
- **With 10 symbols:** 3 + (3 × 10) = 33 calls/bar
- **With 40 symbols:** 3 + (3 × 40) = 123 calls/bar

### Memory Usage
- Minimal: 3 int variables, 1 string array (symbols)
- Negligible impact on script performance

## Rollback Procedure

If needed, revert to previous version:

```bash
git checkout HEAD~1 -- "Pullbackformasyon ve dip_v7.txt"
```

Or manually remove lines:
- **Lines 142-163:** EMA input groups
- **Lines 1823-2004:** EMA module logic

## Success Criteria

✅ **Script compiles** without errors on TradingView
✅ **Existing alerts** unchanged and working
✅ **BUY signals** fire correctly (1H cross + 15m state)
✅ **SELL signals** disabled by default
✅ **Watchlist scan** sends aggregated messages
✅ **Cooldown** prevents spam
✅ **Separate chat_ids** for BUY/SELL working
✅ **40 symbol limit** enforced
✅ **No breaking changes** to existing modules

## Contact

For issues or questions:
- Check README: `EMA_CROSS_MODULE_README.md`
- Review code: Lines 142-163, 1823-2004 in `Pullbackformasyon ve dip_v7.txt`
