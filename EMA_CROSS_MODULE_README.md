# EMA Cross Module - Implementation Summary

## Overview
Added a new EMA Cross module to `Pullbackformasyon ve dip_v7.txt` that provides 1H timeframe signals with 15m confirmation, integrated with existing alert system and watchlist scanning.

## Features Added

### 1. Input Configuration (Lines 142-163)
New input group: **"EMA Cross (1H + 15m Onay)"**

**Core Settings:**
- `ema_enable` - Master switch (default: true)
- `ema_fast` - Fast EMA period (default: 5)
- `ema_slow` - Slow EMA period (default: 137)
- `ema_enable_buy` - Enable BUY signals (default: true)
- `ema_enable_sell` - Enable SELL signals (default: **false** - disabled)
- `ema_buy_chat_id` - Telegram chat ID for BUY alerts (default: same as DIP chat_id)
- `ema_sell_chat_id` - Telegram chat ID for SELL alerts (default: same as SAT chat_id)
- `ema_cooldown_min` - Cooldown period in minutes (default: 60)
- `ema_show_labels` - Show labels on chart (default: true)

**Watchlist Settings:**
- `ema_watch_enable` - Enable watchlist scanning (default: true)
- `ema_watch_prefix` - Symbol prefix (default: "BIST:")
- `ema_watch_symbols` - Comma-separated symbol list (max 40 symbols)
- `ema_watch_buy_chat_id` - Optional separate chat ID for watchlist BUY alerts
- `ema_watch_sell_chat_id` - Optional separate chat ID for watchlist SELL alerts

### 2. Signal Logic (Lines 1823-2004)

**BUY Signal Conditions:**
1. 1H EMA5 crosses ABOVE EMA137 (confirmed bar close only)
2. AND 15m EMA5 > EMA137 (state confirmation, not cross)
3. AND cooldown period has elapsed

**SELL Signal Conditions:**
1. 1H EMA5 crosses BELOW EMA137 (confirmed bar close only)
2. AND 15m EMA5 < EMA137 (state confirmation, not cross)
3. AND cooldown period has elapsed
4. AND `ema_enable_sell` is true (default: false)

### 3. Message Format

**Single Symbol BUY Message:**
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

**Watchlist BUY Message (Aggregated):**
```
⚡ EMA CROSS 1H TARAMA • BUY (AL)

TETİK: 1H EMA5 yukarı kesti EMA137
ONAY: 15m EMA5 > EMA137 (STATE)

HISSELER (3):
• THYAO
• PETKM
• SASA
```

### 4. Integration with Existing System

**Non-Breaking Changes:**
- Uses existing `send_msg()` function
- Follows existing cooldown pattern with timestamp tracking
- Uses existing message formatting utilities (`fmtMintMsg()`, `f_lineJoin()`)
- Added 2 new `alertcondition()` declarations:
  - "EMA CROSS BUY (1H+15m)"
  - "EMA CROSS SELL (1H+15m)"

**Cooldown Mechanism:**
- Separate cooldown tracking for BUY and SELL signals
- Shared cooldown for watchlist scanning (prevents spam)
- Uses same pattern as other modules (timestamp comparison)

### 5. Watchlist Scanning

**Implementation Details:**
- Scans symbol list on every 1H bar close
- Parses comma-separated symbol list at runtime
- Caps at 40 symbols to avoid excessive `request.security` calls
- Uses prefix (e.g., "BIST:") to construct full ticker symbols
- Sends aggregated messages (one for BUY, one for SELL)
- Separate chat IDs supported for watchlist vs single symbol

**Symbol List Format:**
```
THYAO,PETKM,SASA,SAHOL,AKBNK,EREGL,...
```

## Testing Checklist

### Basic Functionality
- [ ] Script compiles without errors on TradingView
- [ ] Existing alerts (DIP, SAT, MTF, E2, DB, SuperDip) still work
- [ ] EMA inputs visible in settings panel
- [ ] Can toggle module on/off

### BUY Signal Testing
- [ ] BUY signal fires when 1H cross up + 15m state confirm
- [ ] BUY message sent to correct chat_id
- [ ] Label appears on chart (green, pointing up)
- [ ] Cooldown prevents spam (60 min default)
- [ ] Alert visible in TradingView alert list

### SELL Signal Testing
- [ ] SELL is disabled by default (no alerts)
- [ ] When enabled, SELL fires when 1H cross down + 15m state confirm
- [ ] SELL message sent to correct chat_id
- [ ] Label appears on chart (red, pointing down)

### Watchlist Testing
- [ ] Watchlist scan triggers on 1H close
- [ ] Multiple matching symbols aggregated in one message
- [ ] Symbol prefix applied correctly (BIST:)
- [ ] Max 40 symbols enforced
- [ ] Optional separate chat_id works

## Configuration Examples

### Example 1: BUY Only (Default)
```
ema_enable = true
ema_enable_buy = true
ema_enable_sell = false  // Default - no SELL alerts
ema_watch_enable = true
```

### Example 2: Both BUY and SELL
```
ema_enable = true
ema_enable_buy = true
ema_enable_sell = true   // Enable SELL alerts
ema_watch_enable = true
```

### Example 3: Watchlist Disabled
```
ema_enable = true
ema_enable_buy = true
ema_enable_sell = false
ema_watch_enable = false  // No watchlist scanning
```

### Example 4: Custom Symbol List (Short)
```
ema_watch_symbols = "THYAO,PETKM,SASA,AKBNK,EREGL"
```

## Technical Details

### request.security Calls
- **Single Symbol:** 3 calls per bar (1H current, 1H previous, 15m current)
- **Watchlist:** 3 calls × N symbols (where N ≤ 40)
- All calls use `barmerge.gaps_off` and `barmerge.lookahead_off` for safety

### Memory Usage
- 2 timestamp variables for cooldown tracking
- 1 timestamp variable for watchlist scan cooldown
- 1 array for symbol parsing (initialized once at `barstate.isfirst`)

### Performance Considerations
- Watchlist parsing happens only at `barstate.isfirst` (once per load)
- Symbol scanning only triggers on 1H confirmed bar close
- Cooldown prevents excessive API calls

## Code Location

**File:** `Pullbackformasyon ve dip_v7.txt`

**Sections Added:**
1. **Lines 142-163:** Input declarations (EMA Cross group, Watchlist group)
2. **Lines 1823-2004:** Core logic, functions, alert sending, alertconditions

**Functions Added:**
- `f_ema_build_msg(isBuy)` - Message builder for single symbol
- `f_ema_parse_symbols()` - Symbol list parser
- `f_ema_check_symbol(tickerStr)` - Per-symbol cross detection

## Migration Notes

If upgrading from a script without this module:

1. **No action required** - Module is self-contained
2. **Existing alerts unaffected** - All prior logic preserved
3. **Default state is safe** - SELL disabled by default
4. **Can disable entirely** - Set `ema_enable = false` to turn off

## Support

### Common Issues

**Q: SELL alerts not firing?**
A: Check that `ema_enable_sell = true` (it's disabled by default)

**Q: Watchlist not scanning?**
A: Ensure `ema_watch_enable = true` and chart is on 1H or higher timeframe

**Q: Too many alerts?**
A: Increase `ema_cooldown_min` or reduce watchlist symbol count

**Q: Wrong symbols in watchlist?**
A: Check `ema_watch_prefix` matches your exchange (e.g., "BIST:", "BINANCE:")

## Version History

- **v7.x (Current):** Added EMA Cross module with 1H+15m confirmation
- Lines added: 203
- Total script lines: 3360
- Alert conditions: 16 total (2 new)
