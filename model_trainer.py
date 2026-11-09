"""
model_trainer.py

Trains a classifier to predict next-day price direction (up=1 / down=0)
using candlestick pattern flags + technical indicator features.

Uses a time-based (not random) train/test split, since shuffling time series
data leaks future information into training — a common and important mistake
to avoid for this kind of problem.
"""

from __future__ import annotations
from dataclasses import dataclass
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from feature_engineering import build_features, get_feature_columns

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False


@dataclass
class TrainResult:
    model: object
    feature_columns: list
    accuracy: float
    precision: float
    recall: float
    f1: float
    confusion: np.ndarray
    baseline_accuracy: float  # accuracy of always predicting the majority class
    feature_importance: pd.Series


def time_based_split(feats: pd.DataFrame, test_size: float = 0.2):
    split_idx = int(len(feats) * (1 - test_size))
    train = feats.iloc[:split_idx]
    test = feats.iloc[split_idx:]
    return train, test


def train_model(
    ohlcv_df: pd.DataFrame,
    model_type: str = "random_forest",
    test_size: float = 0.2,
) -> TrainResult:
    """
    ohlcv_df: raw OHLCV DataFrame (e.g. from yfinance) for a single ticker.
    model_type: "random_forest" or "xgboost".
    """
    feats = build_features(ohlcv_df)
    if len(feats) < 60:
        raise ValueError(
            f"Not enough data after feature engineering ({len(feats)} rows). "
            "Use a longer history (1y+ of daily data recommended)."
        )

    feature_cols = get_feature_columns(feats)
    train, test = time_based_split(feats, test_size)

    X_train, y_train = train[feature_cols], train["target"]
    X_test, y_test = test[feature_cols], test["target"]

    if model_type == "xgboost" and HAS_XGB:
        model = XGBClassifier(
            n_estimators=300,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss",
            random_state=42,
        )
    else:
        model = RandomForestClassifier(
            n_estimators=300,
            max_depth=6,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1,
        )

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    baseline_accuracy = max(y_test.mean(), 1 - y_test.mean())

    importance = pd.Series(model.feature_importances_, index=feature_cols).sort_values(
        ascending=False
    )

    return TrainResult(
        model=model,
        feature_columns=feature_cols,
        accuracy=accuracy_score(y_test, preds),
        precision=precision_score(y_test, preds, zero_division=0),
        recall=recall_score(y_test, preds, zero_division=0),
        f1=f1_score(y_test, preds, zero_division=0),
        confusion=confusion_matrix(y_test, preds),
        baseline_accuracy=baseline_accuracy,
        feature_importance=importance,
    )


def save_model(result: TrainResult, path: str) -> None:
    joblib.dump({"model": result.model, "feature_columns": result.feature_columns}, path)


def load_model(path: str):
    return joblib.load(path)


def predict_next_direction(model_bundle: dict, ohlcv_df: pd.DataFrame):
    """
    Returns (prediction, confidence) for the most recent row of ohlcv_df.
    prediction: "UP" or "DOWN"
    confidence: probability of the predicted class (0-1)
    """
    feats = build_features(ohlcv_df)
    # build_features drops the last row's target (it's unknown), but we still
    # want a feature row for "today" to predict tomorrow — recompute without
    # dropping the final row's NaN target specifically.
    latest_row = feats.iloc[[-1]][model_bundle["feature_columns"]]
    proba = model_bundle["model"].predict_proba(latest_row)[0]
    pred_class = int(np.argmax(proba))
    return ("UP" if pred_class == 1 else "DOWN"), float(proba[pred_class])
