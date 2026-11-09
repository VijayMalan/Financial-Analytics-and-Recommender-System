"""
candlestick_patterns.py

Rule-based candlestick pattern detection using OHLC data.
Each pattern function returns a boolean Series aligned to the input DataFrame index.
These are used both as standalone signals and as binary features fed into the
ML classifier in model_trainer.py.

Expects a DataFrame with columns: Open, High, Low, Close (standard yfinance output).
"""

from __future__ import annotations
import pandas as pd
import numpy as np


def _body(df: pd.DataFrame) -> pd.Series:
    return (df["Close"] - df["Open"]).abs()


def _range(df: pd.DataFrame) -> pd.Series:
    return (df["High"] - df["Low"]).replace(0, np.nan)


def _upper_shadow(df: pd.DataFrame) -> pd.Series:
    return df["High"] - df[["Open", "Close"]].max(axis=1)


def _lower_shadow(df: pd.DataFrame) -> pd.Series:
    return df[["Open", "Close"]].min(axis=1) - df["Low"]


def is_bullish(df: pd.DataFrame) -> pd.Series:
    return df["Close"] > df["Open"]


def is_bearish(df: pd.DataFrame) -> pd.Series:
    return df["Close"] < df["Open"]


def doji(df: pd.DataFrame, body_ratio: float = 0.1) -> pd.Series:
    """Body is a very small fraction of the day's range — market indecision."""
    return _body(df) <= body_ratio * _range(df)


def hammer(df: pd.DataFrame) -> pd.Series:
    """Small body near the top of the range, long lower shadow — bullish reversal signal."""
    body = _body(df)
    lower = _lower_shadow(df)
    upper = _upper_shadow(df)
    return (lower >= 2 * body) & (upper <= body) & (body > 0)


def hanging_man(df: pd.DataFrame) -> pd.Series:
    """Same shape as hammer, but appears after an uptrend — bearish reversal signal."""
    shape = hammer(df)
    prior_uptrend = df["Close"].shift(1) > df["Close"].shift(3)
    return shape & prior_uptrend


def shooting_star(df: pd.DataFrame) -> pd.Series:
    """Small body near the bottom of the range, long upper shadow — bearish reversal signal."""
    body = _body(df)
    lower = _lower_shadow(df)
    upper = _upper_shadow(df)
    return (upper >= 2 * body) & (lower <= body) & (body > 0)


def bullish_engulfing(df: pd.DataFrame) -> pd.Series:
    prev_bearish = is_bearish(df).shift(1)
    curr_bullish = is_bullish(df)
    engulfs = (df["Open"] <= df["Close"].shift(1)) & (df["Close"] >= df["Open"].shift(1))
    return prev_bearish & curr_bullish & engulfs


def bearish_engulfing(df: pd.DataFrame) -> pd.Series:
    prev_bullish = is_bullish(df).shift(1)
    curr_bearish = is_bearish(df)
    engulfs = (df["Open"] >= df["Close"].shift(1)) & (df["Close"] <= df["Open"].shift(1))
    return prev_bullish & curr_bearish & engulfs


def piercing_line(df: pd.DataFrame) -> pd.Series:
    """Bearish candle followed by a bullish candle that closes above the prior candle's midpoint."""
    prev_bearish = is_bearish(df).shift(1)
    curr_bullish = is_bullish(df)
    prev_mid = (df["Open"].shift(1) + df["Close"].shift(1)) / 2
    opens_below = df["Open"] < df["Close"].shift(1)
    closes_above_mid = df["Close"] > prev_mid
    closes_below_prev_open = df["Close"] < df["Open"].shift(1)
    return prev_bearish & curr_bullish & opens_below & closes_above_mid & closes_below_prev_open


def dark_cloud_cover(df: pd.DataFrame) -> pd.Series:
    """Bullish candle followed by a bearish candle that closes below the prior candle's midpoint."""
    prev_bullish = is_bullish(df).shift(1)
    curr_bearish = is_bearish(df)
    prev_mid = (df["Open"].shift(1) + df["Close"].shift(1)) / 2
    opens_above = df["Open"] > df["Close"].shift(1)
    closes_below_mid = df["Close"] < prev_mid
    closes_above_prev_open = df["Close"] > df["Open"].shift(1)
    return prev_bullish & curr_bearish & opens_above & closes_below_mid & closes_above_prev_open


def morning_star(df: pd.DataFrame) -> pd.Series:
    """Three-candle bullish reversal: big bearish, small-bodied middle candle, big bullish."""
    first_bearish = is_bearish(df).shift(2)
    first_body = _body(df).shift(2)
    middle_small = _body(df).shift(1) < 0.3 * first_body
    third_bullish = is_bullish(df)
    third_recovers = df["Close"] > (df["Open"].shift(2) + df["Close"].shift(2)) / 2
    return first_bearish & middle_small & third_bullish & third_recovers


def evening_star(df: pd.DataFrame) -> pd.Series:
    """Three-candle bearish reversal: big bullish, small-bodied middle candle, big bearish."""
    first_bullish = is_bullish(df).shift(2)
    first_body = _body(df).shift(2)
    middle_small = _body(df).shift(1) < 0.3 * first_body
    third_bearish = is_bearish(df)
    third_drops = df["Close"] < (df["Open"].shift(2) + df["Close"].shift(2)) / 2
    return first_bullish & middle_small & third_bearish & third_drops


def three_white_soldiers(df: pd.DataFrame) -> pd.Series:
    """Three consecutive bullish candles, each closing higher than the last."""
    cond = is_bullish(df) & is_bullish(df).shift(1) & is_bullish(df).shift(2)
    rising = (df["Close"] > df["Close"].shift(1)) & (df["Close"].shift(1) > df["Close"].shift(2))
    return cond & rising


def three_black_crows(df: pd.DataFrame) -> pd.Series:
    """Three consecutive bearish candles, each closing lower than the last."""
    cond = is_bearish(df) & is_bearish(df).shift(1) & is_bearish(df).shift(2)
    falling = (df["Close"] < df["Close"].shift(1)) & (df["Close"].shift(1) < df["Close"].shift(2))
    return cond & falling


# Registry used by feature_engineering.py to generate pattern flag columns automatically
PATTERN_FUNCTIONS = {
    "doji": doji,
    "hammer": hammer,
    "hanging_man": hanging_man,
    "shooting_star": shooting_star,
    "bullish_engulfing": bullish_engulfing,
    "bearish_engulfing": bearish_engulfing,
    "piercing_line": piercing_line,
    "dark_cloud_cover": dark_cloud_cover,
    "morning_star": morning_star,
    "evening_star": evening_star,
    "three_white_soldiers": three_white_soldiers,
    "three_black_crows": three_black_crows,
}


def detect_all_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a DataFrame of binary (0/1) columns, one per pattern, aligned to df's index."""
    out = pd.DataFrame(index=df.index)
    for name, fn in PATTERN_FUNCTIONS.items():
        out[f"pattern_{name}"] = fn(df).fillna(False).astype(int)
    return out
