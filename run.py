import os
import re
import argparse
from datetime import datetime
import itertools
from typing import List, Tuple, Dict, Any, Optional

import numpy as np
import pandas as pd

PREFIX = "multimplus"

ENSEMBLE_RE = re.compile(r"^ensemble_multim_(\d{4}-\d{2}-\d{2})\.csv$", re.IGNORECASE)

COL_SYMBOL = "Sembol"
COL_DATE = "Tarih"
COL_PRICE = "Fiyat (Son)"

TARGET = "MaxRet_FWD"
HIT_THR = 15.0  # %15+ in horizon

# default filters you requested
DEFAULT_DAILY_LIMIT = 9.5
DEFAULT_MONTHLY_LIMIT = 30.0


# ----------------- Helpers -----------------
def _read_csv_any(path: str) -> pd.DataFrame:
    for enc in ["utf-8-sig", "utf-8", "cp1254", "latin1"]:
        try:
            df = pd.read_csv(path, encoding=enc, low_memory=False)
            df.columns = [str(c).strip() for c in df.columns]
            return df
        except Exception:
            continue
    df = pd.read_csv(path, low_memory=False)
    df.columns = [str(c).strip() for c in df.columns]
    return df

def _smart_to_numeric(s: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(s):
        return s.astype("float64")
    if pd.api.types.is_numeric_dtype(s):
        return pd.to_numeric(s, errors="coerce")
    x = s.astype(str).str.strip().replace({"nan": np.nan, "None": np.nan, "none": np.nan, "": np.nan})
    x = x.str.replace(r"[^0-9,\.\-]", "", regex=True)
    sm = x.dropna().head(200)
    comma = int(sm.str.contains(r",\d{1,4}$", na=False).sum()) if len(sm) else 0
    dot = int(sm.str.contains(r"\.\d{1,4}$", na=False).sum()) if len(sm) else 0
    if comma > dot:
        x = x.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    else:
        x = x.str.replace(",", "", regex=False)
    return pd.to_numeric(x, errors="coerce")

def ensure_symbol_upper(df: pd.DataFrame) -> pd.DataFrame:
    if COL_SYMBOL in df.columns:
        df[COL_SYMBOL] = df[COL_SYMBOL].astype(str).str.strip().str.upper()
    return df

def ensure_date_str(df: pd.DataFrame, col: str) -> pd.Series:
    return pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")


# ----------------- Step 1: Find ensemble files -----------------
def find_ensemble_files(folder: str) -> List[Tuple[str, str]]:
    cands = []
    for fn in os.listdir(folder):
        m = ENSEMBLE_RE.match(fn)
        if m:
            cands.append((m.group(1), os.path.join(folder, fn)))
    cands.sort(key=lambda x: x[0])
    return cands


# ----------------- Step 2: Backtest dataset -----------------
def build_price_panel(files: List[Tuple[str, str]]) -> pd.DataFrame:
    frames = []
    for d, p in files:
        df = _read_csv_any(p)
        if COL_SYMBOL not in df.columns or COL_PRICE not in df.columns:
            continue
        df = ensure_symbol_upper(df)
        pr = _smart_to_numeric(df[COL_PRICE])
        part = pd.DataFrame({"date": d, COL_SYMBOL: df[COL_SYMBOL], "price": pr})
        part = part.dropna(subset=[COL_SYMBOL, "price"])
        frames.append(part)

    if not frames:
        raise RuntimeError("No usable ensemble files with columns: Sembol + Fiyat (Son)")

    allp = pd.concat(frames, ignore_index=True)
    panel = allp.pivot_table(index=COL_SYMBOL, columns="date", values="price", aggfunc="last")
    panel = panel.sort_index(axis=1)
    return panel

def forward_max_return(sym: str, d: str, panel: pd.DataFrame, dates: List[str], horizon: int) -> float:
    if sym not in panel.index or d not in dates:
        return np.nan
    i = dates.index(d)
    future = dates[i + 1 : i + 1 + horizon]
    if not future:
        return np.nan
    try:
        p0 = float(panel.loc[sym, d])
    except Exception:
        return np.nan
    if not np.isfinite(p0) or p0 <= 0:
        return np.nan
    win = pd.to_numeric(panel.loc[sym, future], errors="coerce").dropna()
    if win.empty:
        return np.nan
    return (float(win.max()) - p0) / p0 * 100.0

def build_backtest_df(files: List[Tuple[str, str]], horizon: int) -> pd.DataFrame:
    dates = [d for d, _ in files]
    panel = build_price_panel(files)

    frames = []
    for d, p in files:
        df = _read_csv_any(p)
        if COL_SYMBOL not in df.columns or COL_PRICE not in df.columns:
            continue
        df = ensure_symbol_upper(df)
        df["Analiz_Tarihi_str"] = d
        df[COL_PRICE] = _smart_to_numeric(df[COL_PRICE])
        frames.append(df)

    df_all = pd.concat(frames, ignore_index=True)
    df_all = df_all.dropna(subset=[COL_SYMBOL, COL_PRICE, "Analiz_Tarihi_str"]).copy()

    df_all[TARGET] = [
        forward_max_return(sym, d, panel, dates, horizon)
        for sym, d in zip(df_all[COL_SYMBOL].tolist(), df_all["Analiz_Tarihi_str"].tolist())
    ]
    return df_all


# ----------------- Step 3: Find best combos (2..4) -----------------
def make_single_rules(df: pd.DataFrame, features: List[str], num_bins: int, min_n: int, topk: int):
    """
    Returns list of tuples:
      (HitRate15, Mean, NegRate, N, col, rule_str, mask, Lift15)
    Sorted by HitRate15 then Mean then low NegRate then N.
    """
    y = df[TARGET]
    base = float((y >= HIT_THR).mean())
    rules = []

    for f in features:
        s = df[f]

        # bool -> ==True/False rules
        if pd.api.types.is_bool_dtype(s):
            for v in [True, False]:
                m = (s == v).fillna(False)
                yy = y[m].dropna()
                if len(yy) < min_n:
                    continue
                hit = float((yy >= HIT_THR).mean())
                neg = float((yy < 0).mean())
                lift = hit / base if base > 0 else np.nan
                rules.append((hit, float(yy.mean()), float(neg), int(len(yy)), f, f"=={v}", m, lift))
            continue

        sn = _smart_to_numeric(s)

        # numeric bins
        if sn.notna().mean() >= 0.7:
            sn2 = sn.dropna()
            if sn2.size < min_n or sn2.nunique() < 5:
                continue

            qs = [float(sn2.quantile(i / num_bins)) for i in range(num_bins + 1)]
            qs = sorted(set([x for x in qs if np.isfinite(x)]))
            if len(qs) < 3:
                continue

            for i in range(len(qs) - 1):
                l, r = qs[i], qs[i + 1]
                m = (sn > l) & (sn <= r)
                yy = y[m].dropna()
                if len(yy) < min_n:
                    continue
                hit = float((yy >= HIT_THR).mean())
                neg = float((yy < 0).mean())
                lift = hit / base if base > 0 else np.nan
                rules.append((hit, float(yy.mean()), float(neg), int(len(yy)), f, f"in_bin({l:.4g},{r:.4g}]", m, lift))
        else:
            vals = s.dropna().unique().tolist()[:30]
            for v in vals:
                m = (s == v).fillna(False)
                yy = y[m].dropna()
                if len(yy) < min_n:
                    continue
                hit = float((yy >= HIT_THR).mean())
                neg = float((yy < 0).mean())
                lift = hit / base if base > 0 else np.nan
                rules.append((hit, float(yy.mean()), float(neg), int(len(yy)), f, f"=={v}", m, lift))

    rules.sort(key=lambda x: (x[0], x[1], -x[2], x[3]), reverse=True)
    return rules[:topk], base

def combo_stats(y: pd.Series, mask: pd.Series, base: float) -> Optional[Dict[str, Any]]:
    yy = y[mask].dropna()
    if yy.empty:
        return None
    hit = float((yy >= HIT_THR).mean())
    neg = float((yy < 0).mean())
    lift = hit / base if base > 0 else np.nan
    return {"N": int(len(yy)), "Mean": float(yy.mean()), "HitRate15": hit, "NegRate": neg, "Lift15": lift}

def find_best_combos(df_backtest: pd.DataFrame, num_bins: int, min_n: int, top_singles: int, max_k: int) -> pd.DataFrame:
    df = df_backtest.dropna(subset=[TARGET]).copy()
    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")
    df = df.dropna(subset=[TARGET])

    y = df[TARGET]
    base = float((y >= HIT_THR).mean())

    ignore = {COL_SYMBOL, COL_DATE, TARGET, "Analiz_Tarihi_str", COL_PRICE}
    features = [c for c in df.columns if c not in ignore and df[c].notna().mean() >= 0.5]

    singles, base = make_single_rules(df, features, num_bins=num_bins, min_n=min_n, topk=top_singles)

    best_rows = []
    for k in range(2, max_k + 1):
        best = None
        best_desc = None

        for idxs in itertools.combinations(range(len(singles)), k):
            m = None
            desc = []
            for j in idxs:
                hit, mean, neg, N, col, rule, mask, lift = singles[j]
                desc.append(f"{col} {rule}")
                m = mask if m is None else (m & mask)

            st = combo_stats(y, m, base)
            if not st or st["N"] < min_n:
                continue

            # objective: HitRate15 first, then Mean, then low NegRate, then N
            key = (st["HitRate15"], st["Mean"], -st["NegRate"], st["N"])
            if best is None or key > best:
                best = key
                best_desc = (" AND ".join(desc), st)

        if best_desc:
            combo_str, st = best_desc
            best_rows.append({"k": k, "combo": combo_str, **st})

    return pd.DataFrame(best_rows).sort_values(["k"])


# ----------------- Step 4: Apply combo on day & build lists -----------------
def parse_combo_string(combo: str) -> List[Tuple[str, str, str]]:
    parts = [p.strip() for p in combo.split("AND")]
    out = []
    for p in parts:
        if " in_bin(" in p:
            col, rest = p.split(" in_bin(", 1)
            rhs = rest.strip()
            if rhs.endswith("]"):
                rhs = rhs[:-1]
            out.append((col.strip(), "in_bin", rhs.strip()))
        elif " ==" in p:
            col, rhs = p.split(" ==", 1)
            out.append((col.strip(), "==", rhs.strip()))
        else:
            out.append((p.strip(), "raw", ""))
    return out

def apply_combo(df: pd.DataFrame, combo: str) -> pd.Series:
    conds = parse_combo_string(combo)
    m = pd.Series(True, index=df.index)

    for col, op, rhs in conds:
        if col not in df.columns:
            return pd.Series(False, index=df.index)

        if op == "==":
            rhs_clean = rhs.strip().strip('"').strip("'")
            if rhs_clean.lower() == "true":
                val = True
            elif rhs_clean.lower() == "false":
                val = False
            else:
                val = rhs_clean

            if pd.api.types.is_bool_dtype(df[col]):
                m &= (df[col] == val).fillna(False)
            else:
                m &= (df[col].astype(str).str.strip() == str(val)).fillna(False)

        elif op == "in_bin":
            try:
                left_s, right_s = [x.strip() for x in rhs.split(",", 1)]
                left = float(left_s)
                right = float(right_s)
            except Exception:
                return pd.Series(False, index=df.index)

            sn = _smart_to_numeric(df[col])
            m &= (sn > left) & (sn <= right)
            m = m.fillna(False)
        else:
            return pd.Series(False, index=df.index)

    return m.fillna(False)

def add_penalties_and_score(df: pd.DataFrame, combo_row: Dict[str, Any]) -> pd.DataFrame:
    out = df.copy()

    for c in ["RAW_SCORE", "Tomorrow_Adj", "TomorrowScore", "MultiTFScore_Norm", "Kirilim_CMF20",
              "RISK_PENALTY", "LOW_RISK_SCORE", "RSI", "Aylık Değişim (%)", "GUNLUK_FARK", "Dipten Uzaklık (%)"]:
        if c in out.columns:
            out[c] = _smart_to_numeric(out[c])

    hit = float(combo_row.get("HitRate15", 0.0))
    mean = float(combo_row.get("Mean", 0.0))
    neg = float(combo_row.get("NegRate", 0.0))

    out["Backtest_BaseScore"] = (100.0 * hit) + (5.0 * mean) - (50.0 * neg)

    boost = pd.Series(0.0, index=out.index)
    if "Tomorrow_Adj" in out.columns:
        boost += out["Tomorrow_Adj"].fillna(0.0) * 0.25
    elif "TomorrowScore" in out.columns:
        boost += out["TomorrowScore"].fillna(0.0) * 0.20
    if "MultiTFScore_Norm" in out.columns:
        boost += out["MultiTFScore_Norm"].fillna(0.0) * 0.05
    if "Kirilim_CMF20" in out.columns:
        boost += out["Kirilim_CMF20"].fillna(0.0) * 1.5
    if "RAW_SCORE" in out.columns:
        boost += out["RAW_SCORE"].fillna(0.0) * 0.05

    penalty = pd.Series(0.0, index=out.index)
    if "RSI" in out.columns:
        rsi = out["RSI"].fillna(0.0)
        penalty += (rsi >= 78).astype(float) * 10.0
        penalty += (rsi >= 85).astype(float) * 15.0
    if "RISK_PENALTY" in out.columns:
        rp = out["RISK_PENALTY"].fillna(0.0)
        penalty += (-rp.clip(upper=0.0)) * 0.10

    out["Backtest_Boost"] = boost
    out["Backtest_Penalty"] = penalty
    out["BacktestRankScore"] = out["Backtest_BaseScore"] + out["Backtest_Boost"] - out["Backtest_Penalty"]

    return out


# ----------------- MAIN -----------------
def main():
    ap = argparse.ArgumentParser(description="One-shot pipeline: backtest -> best combos (2..4) -> excel lists")
    ap.add_argument("--dir", default=".", help="Folder containing ensemble_multim_YYYY-MM-DD.csv files")
    ap.add_argument("--horizon", type=int, default=5, help="Forward horizon in trading days")
    ap.add_argument("--lookback_days", type=int, default=0, help="0=all files, else use last N ensemble days (e.g. 40)")
    ap.add_argument("--num_bins", type=int, default=3)
    ap.add_argument("--min_n", type=int, default=150)
    ap.add_argument("--top_singles", type=int, default=30)
    ap.add_argument("--max_k", type=int, default=4, help="Max combo size (2..max_k). Recommend 4.")
    ap.add_argument("--k_for_list", type=int, default=4, help="Which k to use for list. Must be <= max_k.")
    ap.add_argument("--use_day", choices=["latest", "t-1"], default="latest")
    ap.add_argument("--topn", type=int, default=10)
    ap.add_argument("--daily_limit", type=float, default=DEFAULT_DAILY_LIMIT)
    ap.add_argument("--monthly_limit", type=float, default=DEFAULT_MONTHLY_LIMIT)
    args = ap.parse_args()

    folder = os.path.abspath(args.dir)
    run_date = datetime.now().strftime("%Y-%m-%d")

    # 0) Find ensemble files
    ens_files_all = find_ensemble_files(folder)
    if not ens_files_all:
        raise SystemExit("[Hata] ensemble_multim_*.csv bulunamadı.")

    ens_files_bt = ens_files_all
    if args.lookback_days and args.lookback_days > 0:
        ens_files_bt = ens_files_all[-args.lookback_days:]

    if len(ens_files_bt) < args.horizon + 2:
        raise SystemExit(f"[Hata] Yeterli dosya yok. Bulunan={len(ens_files_bt)} horizon={args.horizon}")

    # 1) Build backtest dataset
    df_backtest = build_backtest_df(ens_files_bt, horizon=args.horizon)
    backtest_path = os.path.join(folder, f"{PREFIX}_backtest_5d_{run_date}.csv")
    df_backtest.to_csv(backtest_path, index=False, encoding="utf-8-sig")
    print(f"[ÇIKTI] {backtest_path}")

    # 2) Find best combos
    df_best = find_best_combos(df_backtest, num_bins=args.num_bins, min_n=args.min_n, top_singles=args.top_singles, max_k=args.max_k)
    if df_best.empty:
        raise SystemExit("[Hata] Combo bulunamadı. (min_n çok yüksek olabilir).")

    best_path = os.path.join(folder, f"{PREFIX}_best_combos_5d_{run_date}.csv")
    df_best.to_csv(best_path, index=False, encoding="utf-8-sig")
    print(f"[ÇIKTI] {best_path}")

    # 3) Choose combo for list
    if args.k_for_list > args.max_k:
        raise SystemExit("[Hata] k_for_list max_k'dan büyük olamaz.")

    ks = sorted(df_best["k"].unique().tolist())
    k_use = args.k_for_list if args.k_for_list in ks else max(ks)
    combo_row = df_best[df_best["k"] == k_use].iloc[0].to_dict()
    combo_str = str(combo_row["combo"])

    print(f"[Bilgi] Liste için seçilen combo k={k_use}: {combo_str}")
    print(f"[Bilgi] Combo stats: N={combo_row.get('N')} Mean={combo_row.get('Mean')} HitRate15={combo_row.get('HitRate15')} NegRate={combo_row.get('NegRate')} Lift15={combo_row.get('Lift15')}")

    # 4) Choose day for list
    if args.use_day == "t-1" and len(ens_files_all) >= 2:
        day_date, day_path = ens_files_all[-2]
    else:
        day_date, day_path = ens_files_all[-1]
    print(f"[Bilgi] Liste üretilecek ensemble dosyası: {day_path}")

    df_day = _read_csv_any(day_path)
    df_day = ensure_symbol_upper(df_day)
    if COL_DATE in df_day.columns:
        df_day[COL_DATE] = ensure_date_str(df_day, COL_DATE)

    # 5) Apply combo
    mask = apply_combo(df_day, combo_str)
    df_matches = df_day[mask].copy()
    df_matches["multimplus_combo_k"] = int(combo_row["k"])
    df_matches["multimplus_combo"] = combo_str
    print(f"[Bilgi] Combo eşleşen satır sayısı (liste günü): {len(df_matches)}")

    # 6) Filters you requested
    if "GUNLUK_FARK" in df_matches.columns:
        df_matches["GUNLUK_FARK"] = _smart_to_numeric(df_matches["GUNLUK_FARK"])
        before = len(df_matches)
        df_matches = df_matches[df_matches["GUNLUK_FARK"].fillna(0.0) < args.daily_limit].copy()
        print(f"[Filtre] GUNLUK_FARK < {args.daily_limit}: {before} -> {len(df_matches)}")

    if "Aylık Değişim (%)" in df_matches.columns:
        df_matches["Aylık Değişim (%)"] = _smart_to_numeric(df_matches["Aylık Değişim (%)"])
        before = len(df_matches)
        df_matches = df_matches[df_matches["Aylık Değişim (%)"].fillna(0.0) <= args.monthly_limit].copy()
        print(f"[Filtre] Aylık Değişim (%) <= {args.monthly_limit}: {before} -> {len(df_matches)}")

    # 7) Score + sort + build lists
    df_scored = add_penalties_and_score(df_matches, combo_row)
    df_sorted = df_scored.sort_values("BacktestRankScore", ascending=False)
    if COL_SYMBOL in df_sorted.columns:
        df_sorted = df_sorted.drop_duplicates(subset=[COL_SYMBOL], keep="first")

    df_normal = df_sorted.head(args.topn).copy()

    df_dip = df_sorted.copy()
    if "LOW_RISK_SCORE" in df_dip.columns:
        df_dip["LOW_RISK_SCORE"] = _smart_to_numeric(df_dip["LOW_RISK_SCORE"])
        thr = df_dip["LOW_RISK_SCORE"].quantile(0.60)
        df_dip = df_dip[df_dip["LOW_RISK_SCORE"].fillna(-np.inf) >= thr]

    if "Dipten Uzaklık (%)" in df_dip.columns:
        df_dip["Dipten Uzaklık (%)"] = _smart_to_numeric(df_dip["Dipten Uzaklık (%)"])
        df_dip = df_dip.sort_values(["BacktestRankScore", "Dipten Uzaklık (%)"], ascending=[False, True])
    else:
        df_dip = df_dip.sort_values("BacktestRankScore", ascending=False)

    if COL_SYMBOL in df_dip.columns:
        df_dip = df_dip.drop_duplicates(subset=[COL_SYMBOL], keep="first")
    df_dip = df_dip.head(args.topn).copy()

    # 8) Excel output (all columns preserved)
    out_xlsx = os.path.join(folder, f"{PREFIX}_listeler_{run_date}.xlsx")
    with pd.ExcelWriter(out_xlsx, engine="openpyxl") as writer:
        df_normal.to_excel(writer, index=False, sheet_name="NORMAL_TOP10")
        df_dip.to_excel(writer, index=False, sheet_name="DIP_TOP10")
        pd.DataFrame([combo_row]).to_excel(writer, index=False, sheet_name="COMBO_USED")
        df_sorted.to_excel(writer, index=False, sheet_name="ALL_MATCHES_SORTED")
        df_matches.to_excel(writer, index=False, sheet_name="ALL_MATCHES_RAW")

    print(f"[ÇIKTI] {out_xlsx}")
    print("[Tamamlandı] run.py pipeline bitti. Başka script çalıştırmana gerek yok.")


if __name__ == "__main__":
    main()