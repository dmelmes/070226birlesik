# AlphaTrend (ALPHA) Implementation Documentation

## Complete Code Reference for "Başarılı ALPHA" Module

This document provides a complete code reference for the AlphaTrend Confirmed BUY module with historical performance gate, as implemented in the V7_5_07226.txt script.

---

## Table of Contents

1. [Overview](#1-overview)
2. [File and Line References](#2-file-and-line-references)
3. [Input Parameters](#3-input-parameters)
4. [Core AlphaTrend Function](#4-core-alphatrend-function)
5. [Global State Variables](#5-global-state-variables)
6. [Helper Functions](#6-helper-functions)
7. [MTF Data Retrieval (4H and 1D)](#7-mtf-data-retrieval-4h-and-1d)
8. [4H Processing Logic](#8-4h-processing-logic)
9. [1D Processing Logic](#9-1d-processing-logic)
10. [Alert Mechanism](#10-alert-mechanism)
11. [Comparison with BANKO KESIŞME AL](#11-comparison-with-banko-kesişme-al)
12. [Technical Implementation Details](#12-technical-implementation-details)

---

## 1. Overview

**Module Name:** AT — AlphaTrend Confirmed BUY Module with Historical Performance Gate

**Purpose:** 
- Detect AlphaTrend confirmed BUY signals on 4H and 1D timeframes
- Track historical performance of signals
- Only send alerts when historical success criteria are met (e.g., 2 of last 3 signals reached +20% target)

**File:** `V7_5_07226.txt`

**Total Code:** ~320 lines (inputs, function, state, logic, alerts)

**Key Innovation:** Historical performance filtering - signals only trigger alerts if past signals have been successful.

---

## 2. File and Line References

### Complete Line Map

| Section | Lines | Description |
|---------|-------|-------------|
| **Inputs** | 2426-2439 | 11 input parameters for module configuration |
| **Core Function** | 2543-2572 | f_alphatrend() - AlphaTrend calculation and signal detection |
| **Global State** | 2577-2585 | State variables for 4H and 1D tracking |
| **Helper Functions** | 2592-2627 | 3 helper functions for outcome tracking |
| **Main Logic Start** | 2630 | if enableAlphaPerf and not safeBoot |
| **4H MTF Retrieval** | 2635-2638 | request.security() call for 4H |
| **1D MTF Retrieval** | 2643-2646 | request.security() call for 1D |
| **4H Processing** | 2651-2691 | 4H evaluation, gate check, alert |
| **1D Processing** | 2696-2736 | 1D evaluation, gate check, alert |
| **Test Ping** | 2739-2743 | Bar close test message |

### Quick Navigation

```
Inputs:          Line 2426-2439
Function:        Line 2543-2572
4H Security:     Line 2635-2638
1D Security:     Line 2643-2646
4H Alert:        Line 2686
1D Alert:        Line 2731
```

---

## 3. Input Parameters

**File Location:** Lines 2426-2439

```pinescript
// Input group definition
grpAT = "AT — AlphaTrend Confirmed BUY"

// 11 configurable parameters:
enableAlphaPerf      = input.bool(false, "AT Module Enable", group=grpAT)
alphaChatId          = input.string("", "AT Telegram chat_id (boş=DEFAULT)", group=grpAT)
alpha_coeff          = input.float(1.0, "AT Multiplier", step=0.1, minval=0.1, group=grpAT)
alpha_AP             = input.int(14, "AT Common Period", minval=1, group=grpAT)
alpha_evalBars_4h    = input.int(120, "AT 4H Eval Bars (~20 sessions)", minval=1, group=grpAT)
alpha_evalBars_1d    = input.int(20, "AT 1D Eval Bars (20 days)", minval=1, group=grpAT)
alpha_targetPct      = input.float(20.0, "AT Target % (max run-up)", step=0.5, minval=0.1, group=grpAT)
alpha_lastN          = input.int(3, "AT Last N signals to track", minval=1, maxval=10, group=grpAT)
alpha_minWins        = input.int(2, "AT Min Wins required", minval=1, maxval=10, group=grpAT)
alpha_sendOn         = input.string("Both", "AT Send alerts on TF", options=["4H","1D","Both"], group=grpAT)
alpha_novolumedata   = input.bool(false, "AT No Volume Data (use RSI)", group=grpAT)
```

### Parameter Details

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `enableAlphaPerf` | false | Master enable switch |
| `alphaChatId` | "" | Telegram chat ID (empty = use default) |
| `alpha_coeff` | 1.0 | AlphaTrend ATR multiplier |
| `alpha_AP` | 14 | Common period for ATR/RSI/MFI |
| `alpha_evalBars_4h` | 120 | 4H evaluation window (~20 sessions) |
| `alpha_evalBars_1d` | 20 | 1D evaluation window (20 days) |
| `alpha_targetPct` | 20.0 | Success threshold (% max run-up) |
| `alpha_lastN` | 3 | Number of signals to track |
| `alpha_minWins` | 2 | Required wins out of lastN |
| `alpha_sendOn` | "Both" | Which TF to send alerts ("4H", "1D", "Both") |
| `alpha_novolumedata` | false | Use RSI instead of MFI if true |

---

## 4. Core AlphaTrend Function

**File Location:** Lines 2543-2572

### Function Signature

```pinescript
f_alphatrend(coeff, AP, novolumedata) =>
    // Returns: [AlphaTrend, confirmedBuy, entryPrice, signalTime]
```

### Complete Implementation

```pinescript
f_alphatrend(coeff, AP, novolumedata) =>
    // Step 1: Calculate ATR
    _ATR = ta.sma(ta.tr, AP)
    
    // Step 2: Calculate upper and lower bands
    _upT = low - _ATR * coeff
    _downT = high + _ATR * coeff
    
    // Step 3: AlphaTrend calculation with condition
    var float _AlphaTrend = na
    _condition = novolumedata ? ta.rsi(close, AP) >= 50 : ta.mfi(hlc3, AP) >= 50
    _AlphaTrend := _condition ? 
                   (_upT < nz(_AlphaTrend[1]) ? nz(_AlphaTrend[1]) : _upT) : 
                   (_downT > nz(_AlphaTrend[1]) ? nz(_AlphaTrend[1]) : _downT)
    
    // Step 4: Detect crossover signals
    _buySignalk = ta.crossover(_AlphaTrend, _AlphaTrend[2])
    _sellSignalk = ta.crossunder(_AlphaTrend, _AlphaTrend[2])
    
    // Step 5: Calculate bars since signals
    _K1 = ta.barssince(_buySignalk)
    _K2 = ta.barssince(_sellSignalk)
    _O1 = ta.barssince(_buySignalk[1])
    _O2 = ta.barssince(_sellSignalk[1])
    
    // Step 6: Confirmed BUY detection
    // Logic: buySignalk[1] and O1[1] > K2 (signal approved on next bar)
    _confirmedBuy = barstate.isconfirmed and _buySignalk[1] and _O1[1] > _K2
    
    // Step 7: Entry price and signal time
    _entryPrice = _confirmedBuy ? close : na
    _signalTime = _confirmedBuy ? time : na
    
    // Return tuple
    [_AlphaTrend, _confirmedBuy, _entryPrice, _signalTime]
```

### Key Logic

**Confirmed BUY Condition:**
```pinescript
_confirmedBuy = barstate.isconfirmed and _buySignalk[1] and _O1[1] > _K2
```

This ensures:
1. `barstate.isconfirmed` - Working with closed bar
2. `_buySignalk[1]` - BUY crossover happened on previous bar
3. `_O1[1] > _K2` - Previous signal is older than last sell signal

**Entry Price:** Close of the confirmation bar (current bar when confirmed)

---

## 5. Global State Variables

**File Location:** Lines 2577-2585

### 4H State Variables

```pinescript
var float at4h_evalEntry = na      // Entry price for current evaluation
var int at4h_evalStartBar = na     // Bar index when evaluation started
var float at4h_evalMaxHigh = na    // Maximum high during evaluation
var array<float> at4h_outcomes = array.new_float(0)  // Historical outcomes array
```

### 1D State Variables

```pinescript
var float at1d_evalEntry = na      // Entry price for current evaluation
var int at1d_evalStartBar = na     // Bar index when evaluation started
var float at1d_evalMaxHigh = na    // Maximum high during evaluation
var array<float> at1d_outcomes = array.new_float(0)  // Historical outcomes array
```

### Purpose

- Track ongoing signal evaluation
- Store historical performance data
- Separate state for each timeframe (4H and 1D)

---

## 6. Helper Functions

**File Location:** Lines 2592-2627

### 6.1 Add Outcome to Array

```pinescript
f_at_add_outcome(tfKey, pct, lastN) =>
    if tfKey == "4H"
        array.unshift(at4h_outcomes, pct)
        while array.size(at4h_outcomes) > lastN
            array.pop(at4h_outcomes)
    else if tfKey == "1D"
        array.unshift(at1d_outcomes, pct)
        while array.size(at1d_outcomes) > lastN
            array.pop(at1d_outcomes)
```

**Purpose:** Add a new outcome percentage to the beginning of the array, trim to lastN

**Parameters:**
- `tfKey`: "4H" or "1D"
- `pct`: Run-up percentage achieved
- `lastN`: Maximum array size

### 6.2 Check Historical Gate

```pinescript
f_at_check_gate(tfKey, targetPct, minWins, lastN) =>
    _arr = tfKey == "4H" ? at4h_outcomes : at1d_outcomes
    _size = array.size(_arr)
    _result = false
    if _size < lastN
        _result := false  // Not enough history, gate fails
    else
        _wins = 0
        for i = 0 to _size - 1
            if array.get(_arr, i) >= targetPct
                _wins += 1
        _result := _wins >= minWins  // Check if enough wins
    _result
```

**Purpose:** Check if historical performance meets requirements

**Logic:**
1. If array size < lastN → FALSE (not enough history)
2. Count how many outcomes >= targetPct
3. Return TRUE if wins >= minWins

**Example:** 
- lastN=3, minWins=2, targetPct=20.0
- Outcomes: [+25%, +22%, +18%]
- Result: 2 wins out of 3 → TRUE (gate passes)

### 6.3 Format Outcomes String

```pinescript
f_at_outcomes_str(tfKey) =>
    _arr = tfKey == "4H" ? at4h_outcomes : at1d_outcomes
    _str = ""
    _size = array.size(_arr)
    if _size > 0
        for i = 0 to _size - 1
            if i > 0
                _str += ", "
            _str += "+" + str.tostring(array.get(_arr, i), "#.#") + "%"
    _str
```

**Purpose:** Format outcomes array as string for alert message

**Output Example:** "+25.3%, +22.1%, +18.7%"

---

## 7. MTF Data Retrieval (4H and 1D)

**File Location:** Lines 2635-2646

### 7.1 4H request.security() Call

**Lines:** 2635-2638

```pinescript
[at4h_AT, at4h_confBuy, at4h_entry, at4h_time] = 
    request.security(syminfo.tickerid, "240", 
                     f_alphatrend(alpha_coeff, alpha_AP, alpha_novolumedata), 
                     barmerge.gaps_off, barmerge.lookahead_off)
```

**Parameters:**
- `syminfo.tickerid`: Current symbol
- `"240"`: 4H timeframe (240 minutes)
- `f_alphatrend(...)`: Function call with parameters
- `barmerge.gaps_off`: Fill gaps in data
- `barmerge.lookahead_off`: No lookahead bias

**Returns:** Tuple of 4 values:
1. `at4h_AT`: AlphaTrend value
2. `at4h_confBuy`: Boolean - confirmed BUY signal
3. `at4h_entry`: Entry price (or na)
4. `at4h_time`: Signal timestamp (or na)

### 7.2 1D request.security() Call

**Lines:** 2643-2646

```pinescript
[at1d_AT, at1d_confBuy, at1d_entry, at1d_time] = 
    request.security(syminfo.tickerid, "D", 
                     f_alphatrend(alpha_coeff, alpha_AP, alpha_novolumedata), 
                     barmerge.gaps_off, barmerge.lookahead_off)
```

**Parameters:**
- `syminfo.tickerid`: Current symbol
- `"D"`: Daily timeframe
- `f_alphatrend(...)`: Function call with parameters
- `barmerge.gaps_off`: Fill gaps in data
- `barmerge.lookahead_off`: No lookahead bias

**Returns:** Tuple of 4 values:
1. `at1d_AT`: AlphaTrend value
2. `at1d_confBuy`: Boolean - confirmed BUY signal
3. `at1d_entry`: Entry price (or na)
4. `at1d_time`: Signal timestamp (or na)

### Key Points

**Total request.security() calls:** 2 (one for 4H, one for 1D)

**Lookback:** NOT explicitly in security call. The f_alphatrend() function uses ta.barssince() which looks back at the current timeframe's bar history.

**Data flow:**
1. security() runs f_alphatrend() on 4H/1D timeframe
2. Function internally calculates AlphaTrend and detects signals
3. Returns tuple with signal data
4. Chart timeframe receives the data and processes it

---

## 8. 4H Processing Logic

**File Location:** Lines 2651-2691

### 8.1 Evaluation Window Update

```pinescript
if not na(at4h_evalEntry)
    // Update max high seen during evaluation
    at4h_evalMaxHigh := math.max(nz(at4h_evalMaxHigh, high), high)
    
    // Calculate bars elapsed
    _barsElapsed = bar_index - at4h_evalStartBar
    
    // Check if evaluation window complete
    if _barsElapsed >= alpha_evalBars_4h
        // Calculate run-up percentage
        _runUpPct = (at4h_evalMaxHigh / at4h_evalEntry - 1) * 100.0
        
        // Add to outcomes array
        f_at_add_outcome("4H", _runUpPct, alpha_lastN)
        
        // Close evaluation
        at4h_evalEntry := na
        at4h_evalStartBar := na
        at4h_evalMaxHigh := na
```

**Lookback Calculation:**
- **Method:** Bar count (bar_index based)
- **Window:** `alpha_evalBars_4h` bars (default: 120)
- **Time equivalent:** ~20 sessions (120 bars ÷ 6 bars/day)
- **Calculation:** `_barsElapsed = bar_index - at4h_evalStartBar`

### 8.2 New Signal Processing

```pinescript
if at4h_confBuy and not na(at4h_entry)
    // Check historical gate
    _gatePass = f_at_check_gate("4H", alpha_targetPct, alpha_minWins, alpha_lastN)
    
    if _gatePass
        // Build alert message
        _prevOutcomes = f_at_outcomes_str("4H")
        _criterionMsg = "Kriter: Son " + str.tostring(alpha_lastN) + " AL'in en az " + 
                        str.tostring(alpha_minWins) + "'si, " + 
                        str.tostring(alpha_evalBars_4h) + " bar (~20 seans) içinde >= %" + 
                        str.tostring(alpha_targetPct, "#.#") + " max yükseliş."
        _msgTitle = "🎯 BAŞARILI 4 SAAT AL (AlphaTrend CONFIRMED)"
        _msgBody = "[" + syminfo.ticker + "] 4H\nFiyat: " + fmtMint(at4h_entry) + 
                   "\n" + _criterionMsg
        if _prevOutcomes != ""
            _msgBody := _msgBody + "\nÖnceki AL sonuçları: " + _prevOutcomes
        _fullMsg = _msgTitle + "\n" + _msgBody
        
        // Determine chat_id
        _at_chatId = alphaChatId == "" ? telegramChatId : alphaChatId
        
        // Send event with deterministic ID
        _eventId = "ATCONF_BUY_4H_" + str.tostring(at4h_time)
        send_event(_eventId, _fullMsg, _at_chatId, alert.freq_once_per_bar_close)
    
    // Start new evaluation tracking
    at4h_evalEntry := at4h_entry
    at4h_evalStartBar := bar_index
    at4h_evalMaxHigh := high
```

### 8.3 Signal Trigger Conditions

**Condition 1: Confirmed BUY received from security()**
```pinescript
at4h_confBuy and not na(at4h_entry)
```

**Condition 2: Historical gate passes**
```pinescript
_gatePass = f_at_check_gate("4H", alpha_targetPct, alpha_minWins, alpha_lastN)
```

**Combined:** Signal fires ONLY if both conditions are TRUE

**Alert Timing:** `alert.freq_once_per_bar_close` - Fires once when bar closes

---

## 9. 1D Processing Logic

**File Location:** Lines 2696-2736

### Similar to 4H but with key differences:

**Evaluation Window:**
- **Bars:** `alpha_evalBars_1d` (default: 20)
- **Time:** 20 days
- **Message:** "20 gün (~20 gün)"

**Message Title:**
```pinescript
_msgTitle = "🎯 BAŞARILI 1 GÜN AL (AlphaTrend CONFIRMED)"
```

**Event ID:**
```pinescript
_eventId = "ATCONF_BUY_1D_" + str.tostring(at1d_time)
```

**Otherwise:** Identical logic to 4H processing

---

## 10. Alert Mechanism

### 10.1 Event ID Format

**4H:**
```pinescript
_eventId = "ATCONF_BUY_4H_" + str.tostring(at4h_time)
```
Example: `ATCONF_BUY_4H_1707649200000`

**1D:**
```pinescript
_eventId = "ATCONF_BUY_1D_" + str.tostring(at1d_time)
```
Example: `ATCONF_BUY_1D_1707649200000`

### 10.2 Deduplication

**Method:** Time-based event ID

- Uses signal timestamp from higher timeframe
- Same signal cannot trigger multiple alerts (same ID)
- send_event() handles dedup via sentEventIdsArr

### 10.3 Alert Frequency

```pinescript
alert.freq_once_per_bar_close
```

**Behavior:**
- Fires only when bar closes on chart timeframe
- No intra-bar repainting
- Confirmed signal only

### 10.4 Chat ID Routing

```pinescript
_at_chatId = alphaChatId == "" ? telegramChatId : alphaChatId
```

**Logic:**
- If alphaChatId is empty → use default telegramChatId
- If alphaChatId is set → use dedicated Alpha chat
- Allows separate chat for AlphaTrend signals

### 10.5 Message Format

**Example 4H Message:**
```
🎯 BAŞARILI 4 SAAT AL (AlphaTrend CONFIRMED)
[BTCUSDT] 4H
Fiyat: 45,234.50
Kriter: Son 3 AL'in en az 2'si, 120 bar (~20 seans) içinde >= %20.0 max yükseliş.
Önceki AL sonuçları: +25.3%, +22.1%, +18.7%
```

---

## 11. Comparison with BANKO KESIŞME AL

### 11.1 BANKO AL Implementation

**File Location:** Lines 1640-1643, 2029-2033

#### Signal Detection (Line 1643)

```pinescript
evLInt_Confirmed = confirmWrap(includeLongIntersect and longIntersectAlert)
```

**Where:**
- `includeLongIntersect`: Input parameter (boolean)
- `longIntersectAlert`: Calculated earlier based on supertrend intersection
- `confirmWrap()`: Wrapper function that checks `barstate.isconfirmed`

#### Allow Flag (Line 1709)

```pinescript
allowLInt_Confirmed = fAllow(evLInt_Confirmed, dayLInt, tLInt) and not buyBlockedByPct
```

**Where:**
- `fAllow()`: Checks event, day filter, time filter
- `buyBlockedByPct`: Blocks if recent AL within percentage range

#### Alert Sending (Lines 2029-2032)

```pinescript
if allowLInt_Confirmed
    _bankoConfMsg = "✓ BANKO KESİŞME AL [CONFIRMED]\n[" + syminfo.ticker + "] [" + 
                    f_tf_label(timeframe.period) + "]\nFiyat: " + fmtMint(close) + 
                    "\n✅ Kesin sinyal - Bar kapatıldı" + f_prev_bullish_note()
    _bankoConfId = "BANKO_CONFIRMED_" + str.tostring(time)
    send_event(_bankoConfId, _bankoConfMsg, telegramChatIdMtfBanko, alert.freq_once_per_bar_close)
```

### 11.2 Similarities with AlphaTrend

| Aspect | BANKO AL | AlphaTrend |
|--------|----------|------------|
| **Confirmation** | confirmWrap() + barstate.isconfirmed | barstate.isconfirmed in function |
| **Event ID** | "BANKO_CONFIRMED_" + time | "ATCONF_BUY_4H_" + time |
| **Alert Freq** | alert.freq_once_per_bar_close | alert.freq_once_per_bar_close |
| **Dedup** | Time-based event ID | Time-based event ID |
| **Chat routing** | telegramChatIdMtfBanko | alphaChatId or default |
| **Timing** | Bar close only | Bar close only |

### 11.3 Differences

| Aspect | BANKO AL | AlphaTrend |
|--------|----------|------------|
| **Signal source** | Chart TF only | MTF (4H/1D via security()) |
| **Logic** | Supertrend intersection | AlphaTrend crossover + confirmation |
| **Historical filter** | None | Yes (requires past success) |
| **Evaluation** | Immediate | Tracks 120/20 bars post-signal |
| **Multiple TF** | No | Yes (4H and 1D separate) |
| **Learning mode** | No | Yes (needs N signals first) |

### 11.4 Key Innovation

**AlphaTrend adds historical performance filtering:**

1. **BANKO AL:** Signal → Allow checks → Alert
2. **AlphaTrend:** Signal → Historical gate → Alert

**Example:**
- BANKO: If supertrend intersects, send alert
- Alpha: If AlphaTrend confirms AND last 2 of 3 signals were successful, send alert

---

## 12. Technical Implementation Details

### 12.1 Bar State Usage

**In f_alphatrend() function:**
```pinescript
_confirmedBuy = barstate.isconfirmed and _buySignalk[1] and _O1[1] > _K2
```

**Effect:**
- Only triggers on confirmed (closed) bars
- No intra-bar repainting
- Signal is "locked in" after bar closes

### 12.2 Lookback Methodology

**Type:** Bar count based (not timestamp)

**4H Example:**
```pinescript
_barsElapsed = bar_index - at4h_evalStartBar
if _barsElapsed >= alpha_evalBars_4h  // 120 bars
```

**Why bar count?**
- Consistent across different chart timeframes
- Works on any chart resolution (1m, 5m, 1h, etc.)
- Independent of calendar days/weekends

**Conversion:**
- 4H: 120 bars ≈ 20 sessions (120 bars ÷ 6 4H bars/day)
- 1D: 20 bars = 20 trading days

### 12.3 Performance Tracking Flow

**Step 1: New Signal Arrives**
```pinescript
if at4h_confBuy and not na(at4h_entry)
```

**Step 2: Check Historical Gate**
```pinescript
_gatePass = f_at_check_gate("4H", alpha_targetPct, alpha_minWins, alpha_lastN)
```

**Step 3: If Gate Passes → Send Alert**
```pinescript
if _gatePass
    send_event(_eventId, _fullMsg, _at_chatId, alert.freq_once_per_bar_close)
```

**Step 4: Start Tracking This Signal**
```pinescript
at4h_evalEntry := at4h_entry
at4h_evalStartBar := bar_index
at4h_evalMaxHigh := high
```

**Step 5: Track Max High Every Bar**
```pinescript
if not na(at4h_evalEntry)
    at4h_evalMaxHigh := math.max(nz(at4h_evalMaxHigh, high), high)
```

**Step 6: When Window Completes**
```pinescript
if _barsElapsed >= alpha_evalBars_4h
    _runUpPct = (at4h_evalMaxHigh / at4h_evalEntry - 1) * 100.0
    f_at_add_outcome("4H", _runUpPct, alpha_lastN)
```

**Step 7: Next Signal Uses This History**
```pinescript
// Next time at4h_confBuy triggers, gate check will include this outcome
```

### 12.4 Historical Success Rate Calculation

**Formula:**
```pinescript
_runUpPct = (at4h_evalMaxHigh / at4h_evalEntry - 1) * 100.0
```

**Example:**
- Entry: 100.00
- Max high in 120 bars: 125.00
- Run-up: (125.00 / 100.00 - 1) * 100 = +25.0%

**Success criteria:**
```pinescript
if array.get(_arr, i) >= targetPct  // e.g., 25.0% >= 20.0% → WIN
```

**Gate logic:**
```pinescript
_wins >= minWins  // e.g., 2 wins >= 2 required → PASS
```

### 12.5 Pine Script v5 Compatibility

**Issue:** Pine v5 doesn't support typed array parameters

**Solution:** Use tfKey parameter instead
```pinescript
// NOT: f_at_add_outcome(array<float> arr, pct, lastN)
// YES: f_at_add_outcome(tfKey, pct, lastN)
```

**Global arrays:**
```pinescript
var array<float> at4h_outcomes = array.new_float(0)
var array<float> at1d_outcomes = array.new_float(0)
```

**Selection in function:**
```pinescript
_arr = tfKey == "4H" ? at4h_outcomes : at1d_outcomes
```

### 12.6 Request Count Optimization

**Total security() calls:** 2
- One for 4H
- One for 1D

**No redundant calls:**
- Results stored in variables
- Reused throughout processing
- Minimal performance impact

**Best practice:** Only retrieve what's needed, when needed

---

## Summary

### Quick Reference Card

**Module:** AlphaTrend Confirmed BUY with Historical Performance Gate

**File:** V7_5_07226.txt, Lines 2426-2743

**request.security() calls:**
1. Line 2636-2638: 4H data retrieval
2. Line 2644-2646: 1D data retrieval

**Lookback method:**
- Bar count based (`bar_index - startBar`)
- 4H: 120 bars (~20 sessions)
- 1D: 20 bars (20 days)

**Signal conditions:**
1. AlphaTrend confirmed BUY on 4H/1D (via security())
2. Historical gate passes (e.g., 2 of last 3 reached +20%)

**Alert trigger:**
- Bar close only (`alert.freq_once_per_bar_close`)
- Dedup via time-based event ID
- Confirmed, no repainting

**Comparison to BANKO AL:**
- Similar: Bar close confirmation, dedup, alert mechanism
- Different: MTF retrieval, historical filtering, evaluation tracking

---

## Additional Notes

### Testing Recommendations

1. **Enable module:** `enableAlphaPerf = true`
2. **Set chat ID:** `alphaChatId = "your-chat-id"`
3. **Choose TF:** `alpha_sendOn = "Both"`
4. **Wait for history:** First 3 signals build history (no alerts sent)
5. **After 3 signals:** If 2+ were successful, alerts will fire

### Troubleshooting

**No alerts?**
- Check `enableAlphaPerf = true`
- Check `safeBoot = false`
- Verify historical gate (might need 3+ signals first)
- Check outcomes array size

**Too many alerts?**
- Increase `alpha_minWins` (e.g., 3 of 3)
- Increase `alpha_targetPct` (e.g., 25%)
- Reduce timeframes (only 1D)

**Want more alerts?**
- Decrease `alpha_minWins` (e.g., 1 of 3)
- Decrease `alpha_targetPct` (e.g., 15%)
- Enable both timeframes

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-14  
**Author:** System Documentation  
**Purpose:** Complete code reference for AlphaTrend implementation
