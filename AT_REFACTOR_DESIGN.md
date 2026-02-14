# AlphaTrend Module Refactor - Design Document

## PR #4: Fix MTF Evaluation Bug & Implement Win-Rate Gate

### Problem Statement

**Critical Bug**: Current implementation evaluates 4H/1D signal success using chart TF data:
- Uses chart `high` instead of HTF `high`
- Uses chart `bar_index` instead of HTF `bar_index`
- Result: 4H signal on 1H chart measures success with 1H bars (wrong!)

**Gate System**: Current "last N signals" approach is too rigid. Win-rate based gate is more statistically sound.

---

## Solution Design

### 1. Move Evaluation Inside HTF Context

**Key Insight**: `request.security()` executes the function in HTF context. We must do ALL evaluation there.

**Old (WRONG)**:
```pinescript
// Chart TF code:
if at4h_confBuy
    // Update eval with CHART high and CHART bar_index ❌
    at4h_evalMaxHigh := math.max(at4h_evalMaxHigh, high)  // Chart high!
    _barsElapsed = bar_index - at4h_evalStartBar          // Chart bar_index!
```

**New (CORRECT)**:
```pinescript
// Inside f_at_engine() which runs in HTF:
f_at_engine(...) =>
    // All state management here, using HTF high and HTF bar_index ✅
    var float _evalEntry = na
    var int _evalStartBar = na
    var float _evalMaxHigh = na
    
    if not na(_evalEntry)
        _evalMaxHigh := math.max(_evalMaxHigh, high)  // HTF high! ✅
        _barsElapsed = bar_index - _evalStartBar      // HTF bar_index! ✅
```

---

## Implementation Steps

### Step 1: Update Input Parameters

**Add new parameters**:
```pinescript
// Win-rate based gate parameters
alpha_histMinSamples = input.int(20, "AT Min History Samples", minval=1, group=grpAT)
alpha_histWinRateMin = input.float(0.55, "AT Min Win Rate", step=0.05, minval=0, maxval=1, group=grpAT)
alpha_histMaxSamples = input.int(100, "AT Max History Samples", minval=10, group=grpAT)

// Gate behavior when history insufficient
alpha_gateWhenInsufficient = input.string("Pass", "AT Gate When Insufficient History", 
                                          options=["Pass","Fail"], group=grpAT)

// Debug mode
alpha_debug = input.bool(false, "AT Debug Mode", group=grpAT)

// Allow historical alerts (override realtime-only)
alpha_allowHistoricalAlerts = input.bool(false, "AT Allow Historical Alerts", group=grpAT)
```

**Update existing defaults**:
```pinescript
alpha_evalBars_4h = input.int(90, "AT 4H Eval Bars (~15 days)", minval=1, group=grpAT)
alpha_evalBars_1d = input.int(15, "AT 1D Eval Bars (15 days)", minval=1, group=grpAT)
```

**Remove obsolete**:
```pinescript
// Remove alpha_lastN
// Remove alpha_minWins
```

---

### Step 2: Create HTF Engine Function

This is the core of the refactor. The engine runs entirely in HTF context.

```pinescript
// f_at_engine() - Runs in HTF context (4H or 1D)
// Returns: [AT, confBuy, entry, time, gatePass, samples, wins, winRate, lastOutcome]
f_at_engine(tfKey, coeff, AP, novolumedata, evalBars, targetPct, 
            histMinSamples, histWinRateMin, histMaxSamples, gateWhenInsufficient) =>
    
    // ===== 1. Calculate AlphaTrend Signal =====
    _ATR = ta.sma(ta.tr, AP)
    _upT = low - _ATR * coeff
    _downT = high + _ATR * coeff
    
    var float _AlphaTrend = na
    _condition = novolumedata ? ta.rsi(close, AP) >= 50 : ta.mfi(hlc3, AP) >= 50
    _AlphaTrend := _condition ? 
                   (_upT < nz(_AlphaTrend[1]) ? nz(_AlphaTrend[1]) : _upT) : 
                   (_downT > nz(_AlphaTrend[1]) ? nz(_AlphaTrend[1]) : _downT)
    
    // Buy/Sell signals
    _buySignalk = ta.crossover(_AlphaTrend, _AlphaTrend[2])
    _sellSignalk = ta.crossunder(_AlphaTrend, _AlphaTrend[2])
    
    // Bars since signals
    _K1 = ta.barssince(_buySignalk)
    _K2 = ta.barssince(_sellSignalk)
    _O1 = ta.barssince(_buySignalk[1])
    _O2 = ta.barssince(_sellSignalk[1])
    
    // Confirmed BUY
    _confirmedBuy = barstate.isconfirmed and _buySignalk[1] and _O1[1] > _K2
    _entryPrice = _confirmedBuy ? close : na
    _signalTime = _confirmedBuy ? time : na
    
    // ===== 2. Evaluation State (HTF context!) =====
    var float _evalEntry = na
    var int _evalStartBar = na
    var float _evalMaxHigh = na
    var array<float> _history = array.new_float(0)
    
    // ===== 3. Update Ongoing Evaluation =====
    if not na(_evalEntry)
        // Track max high in HTF context ✅
        _evalMaxHigh := math.max(_evalMaxHigh, high)
        
        // Calculate elapsed HTF bars ✅
        _barsElapsed = bar_index - _evalStartBar
        
        // Check if evaluation window complete
        if _barsElapsed >= evalBars
            // Calculate run-up percentage
            _runUpPct = (_evalMaxHigh / _evalEntry - 1) * 100.0
            
            // Add to history (most recent first)
            array.unshift(_history, _runUpPct)
            
            // Trim to max samples
            while array.size(_history) > histMaxSamples
                array.pop(_history)
            
            // Reset evaluation state
            _evalEntry := na
            _evalStartBar := na
            _evalMaxHigh := na
    
    // ===== 4. Calculate Win Rate and Gate =====
    _samples = array.size(_history)
    _wins = 0
    
    // Count wins
    for i = 0 to _samples - 1
        if array.get(_history, i) >= targetPct
            _wins += 1
    
    // Calculate win rate
    _winRate = _samples > 0 ? _wins / _samples : 0.0
    
    // Gate decision
    _gatePass = false
    if _samples >= histMinSamples
        // Sufficient history: check win rate
        _gatePass := _winRate >= histWinRateMin
    else
        // Insufficient history: use default behavior
        _gatePass := gateWhenInsufficient == "Pass"
    
    // ===== 5. Start New Evaluation on Signal =====
    if _confirmedBuy and not na(_entryPrice)
        _evalEntry := _entryPrice
        _evalStartBar := bar_index  // HTF bar_index! ✅
        _evalMaxHigh := high         // HTF high! ✅
    
    // ===== 6. Prepare Return Values =====
    _lastOutcome = _samples > 0 ? array.get(_history, 0) : na
    
    // Return tuple
    [_AlphaTrend, _confirmedBuy, _entryPrice, _signalTime, 
     _gatePass, _samples, _wins, _winRate, _lastOutcome]
```

---

### Step 3: Update Main Logic

**Remove all global state variables** (now inside engine):
```pinescript
// DELETE these lines:
// var float at4h_evalEntry = na
// var int at4h_evalStartBar = na
// var float at4h_evalMaxHigh = na
// var array<float> at4h_outcomes = array.new_float(0)
// 
// var float at1d_evalEntry = na
// var int at1d_evalStartBar = na
// var float at1d_evalMaxHigh = na
// var array<float> at1d_outcomes = array.new_float(0)
```

**Remove old helper functions** (now integrated in engine):
```pinescript
// DELETE:
// f_at_add_outcome()
// f_at_check_gate()
// f_at_outcomes_str() - keep but modify
```

**New 4H retrieval**:
```pinescript
[at4h_AT, at4h_confBuy, at4h_entry, at4h_time, 
 at4h_gatePass, at4h_samples, at4h_wins, at4h_winRate, at4h_lastOutcome] = 
    request.security(syminfo.tickerid, "240", 
                     f_at_engine("4H", alpha_coeff, alpha_AP, alpha_novolumedata,
                                 alpha_evalBars_4h, alpha_targetPct,
                                 alpha_histMinSamples, alpha_histWinRateMin,
                                 alpha_histMaxSamples, alpha_gateWhenInsufficient),
                     barmerge.gaps_off, barmerge.lookahead_off)
```

**New 1D retrieval**:
```pinescript
[at1d_AT, at1d_confBuy, at1d_entry, at1d_time,
 at1d_gatePass, at1d_samples, at1d_wins, at1d_winRate, at1d_lastOutcome] = 
    request.security(syminfo.tickerid, "D", 
                     f_at_engine("1D", alpha_coeff, alpha_AP, alpha_novolumedata,
                                 alpha_evalBars_1d, alpha_targetPct,
                                 alpha_histMinSamples, alpha_histWinRateMin,
                                 alpha_histMaxSamples, alpha_gateWhenInsufficient),
                     barmerge.gaps_off, barmerge.lookahead_off)
```

**Simplified 4H alert logic**:
```pinescript
if alpha_sendOn == "4H" or alpha_sendOn == "Both"
    // Signal found AND gate passes
    if at4h_confBuy and at4h_gatePass and not na(at4h_entry)
        // Build message
        _winRateStr = str.tostring(at4h_winRate * 100, "#.#")
        _criterionMsg = "Başarı oranı: %" + _winRateStr + " (min %" + 
                        str.tostring(alpha_histWinRateMin * 100, "#.#") + 
                        "), Örneklem: " + str.tostring(at4h_samples) + " sinyal"
        
        _msgTitle = "🎯 BAŞARILI 4 SAAT AL (AlphaTrend)"
        _msgBody = "[" + syminfo.ticker + "] 4H\n" +
                   "Fiyat: " + fmtMint(at4h_entry) + "\n" +
                   _criterionMsg
        
        if not na(at4h_lastOutcome)
            _msgBody := _msgBody + "\nSon sonuç: +" + 
                        str.tostring(at4h_lastOutcome, "#.#") + "%"
        
        _fullMsg = _msgTitle + "\n" + _msgBody
        
        // Chat ID
        _at_chatId = alphaChatId == "" ? telegramChatId : alphaChatId
        
        // Send event
        _eventId = "ATCONF_BUY_4H_" + str.tostring(at4h_time)
        send_event(_eventId, _fullMsg, _at_chatId, alert.freq_once_per_bar_close)
```

**Simplified 1D alert logic**: (similar to 4H)

---

### Step 4: Add Debug Mode

```pinescript
// Debug table (only if enabled)
if alpha_debug
    var table debugTable = table.new(position.top_right, 4, 10, 
                                      border_width=1, border_color=color.gray)
    
    // Header
    table.cell(debugTable, 0, 0, "AlphaTrend Debug", 
               text_color=color.white, bgcolor=color.blue)
    table.merge_cells(debugTable, 0, 0, 3, 0)
    
    // 4H Section
    table.cell(debugTable, 0, 1, "4H Status", bgcolor=color.gray)
    table.merge_cells(debugTable, 0, 1, 3, 1)
    
    table.cell(debugTable, 0, 2, "Confirmed BUY")
    table.cell(debugTable, 1, 2, at4h_confBuy ? "✓ YES" : "✗ NO",
               text_color=at4h_confBuy ? color.green : color.red)
    
    table.cell(debugTable, 0, 3, "Samples")
    table.cell(debugTable, 1, 3, str.tostring(at4h_samples))
    
    table.cell(debugTable, 0, 4, "Wins")
    table.cell(debugTable, 1, 4, str.tostring(at4h_wins))
    
    table.cell(debugTable, 0, 5, "Win Rate")
    _wrStr = str.tostring(at4h_winRate * 100, "#.#") + "%"
    table.cell(debugTable, 1, 5, _wrStr,
               text_color=at4h_winRate >= alpha_histWinRateMin ? color.green : color.orange)
    
    table.cell(debugTable, 0, 6, "Gate Pass")
    table.cell(debugTable, 1, 6, at4h_gatePass ? "✓ PASS" : "✗ FAIL",
               text_color=at4h_gatePass ? color.green : color.red)
    
    table.cell(debugTable, 0, 7, "Last Outcome")
    _loStr = not na(at4h_lastOutcome) ? 
             "+" + str.tostring(at4h_lastOutcome, "#.#") + "%" : "N/A"
    table.cell(debugTable, 1, 7, _loStr)
    
    // Warning if insufficient samples
    if at4h_samples < alpha_histMinSamples
        table.cell(debugTable, 0, 8, "⚠️ History Insufficient", 
                   text_color=color.orange, bgcolor=color.new(color.yellow, 80))
        table.merge_cells(debugTable, 0, 8, 3, 8)
        _warnText = str.tostring(at4h_samples) + "/" + 
                    str.tostring(alpha_histMinSamples) + " samples"
        table.cell(debugTable, 0, 9, _warnText, text_color=color.orange)
        table.merge_cells(debugTable, 0, 9, 3, 9)
    
    // 1D Section (similar, starting at row 10)
    // ... (add similar cells for 1D)
```

---

## Testing Checklist

### Test 1: HTF Evaluation Independence
1. Load script on 1H chart with 4H alert enabled
2. Note outcomes array
3. Change to 5m chart
4. Outcomes should be IDENTICAL (same 4H highs used)
5. ✅ PASS if outcomes don't change with chart TF

### Test 2: Win Rate Gate
1. Set histMinSamples = 5, winRateMin = 0.6
2. Simulate 10 signals with 5 wins, 5 losses
3. Win rate = 50% < 60%
4. ✅ PASS if gate blocks alert

### Test 3: Insufficient History Behavior
1. Set histMinSamples = 20, gateWhenInsufficient = "Pass"
2. Fresh symbol with only 5 historical signals
3. ✅ PASS if alert fires (5 < 20 but Pass mode)
4. Change to "Fail"
5. ✅ PASS if alert blocked

### Test 4: Debug Mode
1. Enable alpha_debug = true
2. ✅ PASS if table shows:
   - Samples count
   - Win rate percentage
   - Gate pass status
   - "Insufficient history" warning when needed

### Test 5: Watchlist Scan
1. Create 500-symbol watchlist
2. Run with histMinSamples = 20, gateWhenInsufficient = "Pass"
3. ✅ PASS if alerts fire for valid signals even without full history

---

## Token Budget

**Current**: ~2,764 lines

**Changes**:
- Remove: ~150 lines (old global state, old helpers, old eval logic)
- Add: ~200 lines (engine function, debug mode, new params)
- Net: +50 lines (~+500 tokens)

**Estimated new total**: ~2,814 lines (~78,500 tokens)
**Buffer**: ~1,500 tokens

✅ **Within 80k limit**

---

## Migration Notes

**For users upgrading**:
1. `alpha_lastN` and `alpha_minWins` removed → Use `alpha_histMinSamples` and `alpha_histWinRateMin`
2. Default eval bars changed: 4H=120→90, 1D=20→15
3. History resets (new storage format)
4. Debug mode available for troubleshooting
5. Outcomes now HTF-independent (correct behavior)

---

**Status**: Design complete, ready for implementation
