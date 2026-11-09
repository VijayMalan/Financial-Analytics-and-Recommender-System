"""
feature_engineering.py

Builds the feature matrix used by the next-day up/down classifier:
  - Candlestick pattern flags (from candlestick_patterns.py)
  - Price/return based features
  - Volatility features
  - Volume features
  - Standard technical indicators (RSI, MACD, moving averages)

Target label: 1 if next day's Close > today's Close, else 0.
"""

from __future__ import annotations
import pandas as pd
import numpy as np

from candlestick_patterns import detect_all_patterns


def _rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)


def _macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    df must have columns: Open, High, Low, Close, Volume (standard yfinance download).
    Returns a feature DataFrame plus a 'target' column (next-day up=1/down=0),
    with any rows containing NaNs (from indicator warm-up or the final unlabeled row) dropped.
    """
    data = df.copy()
    data.columns = [c.capitalize() if isinstance(c, str) else c for c in data.columns]

    feats = pd.DataFrame(index=data.index)

    # --- Return / price-action features ---
    feats["return_1d"] = data["Close"].pct_change(1)
    feats["return_3d"] = data["Close"].pct_change(3)
    feats["return_5d"] = data["Close"].pct_change(5)
    feats["body_pct"] = (data["Close"] - data["Open"]) / data["Open"]
    feats["high_low_range_pct"] = (data["High"] - data["Low"]) / data["Close"]
    feats["close_position_in_range"] = (data["Close"] - data["Low"]) / (
        (data["High"] - data["Low"]).replace(0, np.nan)
    )

    # --- Trend / moving average features ---
    feats["sma_5"] = data["Close"].rolling(5).mean()
    feats["sma_10"] = data["Close"].rolling(10).mean()
    feats["sma_20"] = data["Close"].rolling(20).mean()
    feats["close_vs_sma5"] = data["Close"] / feats["sma_5"] - 1
    feats["close_vs_sma20"] = data["Close"] / feats["sma_20"] - 1
    feats["sma5_vs_sma20"] = feats["sma_5"] / feats["sma_20"] - 1

    # --- Volatility features ---
    feats["volatility_5d"] = feats["return_1d"].rolling(5).std()
    feats["volatility_10d"] = feats["return_1d"].rolling(10).std()

    # --- Volume features ---
    if "Volume" in data.columns:
        feats["volume_change_1d"] = data["Volume"].pct_change(1)
        feats["volume_vs_avg10"] = data["Volume"] / data["Volume"].rolling(10).mean() - 1

    # --- Momentum indicators ---
    feats["rsi_14"] = _rsi(data["Close"], 14)
    macd_line, signal_line, hist = _macd(data["Close"])
    feats["macd"] = macd_line
    feats["macd_signal"] = signal_line
    feats["macd_hist"] = hist

    # --- Candlestick pattern flags ---
    pattern_flags = detect_all_patterns(data)
    feats = pd.concat([feats, pattern_flags], axis=1)

    # --- Target: next day up (1) / down (0) ---
    feats["target"] = (data["Close"].shift(-1) > data["Close"]).astype(int)

    feats = feats.replace([np.inf, -np.inf], np.nan).dropna()
    return feats


FEATURE_COLUMNS = None  # populated at import time below for convenience


def get_feature_columns(feats: pd.DataFrame) -> list[str]:
    """All columns except the target — the actual model input columns."""
    return [c for c in feats.columns if c != "target"]
