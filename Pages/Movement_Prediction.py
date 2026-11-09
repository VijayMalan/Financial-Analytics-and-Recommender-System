import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

from model_trainer import train_model, predict_next_direction
from candlestick_patterns import detect_all_patterns

st.title("Next-Day Movement Prediction")
st.write(
    "Trains a classifier on candlestick patterns and technical indicators "
    "to predict whether tomorrow's close will be higher or lower than today's."
)
st.divider()

# --- Reuse the same index/company selectors as the rest of the app ---
nifty_50_dict = {
    'Reliance': 'RELIANCE.NS',
    'TCS': 'TCS.NS',
    'Infosys': 'INFY.NS',
    'HDFC Bank': 'HDFCBANK.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    # ... plug in the full dict shared across pages (or import from a shared config module)
}

company_name = st.sidebar.selectbox("Please Select a Company", list(nifty_50_dict.keys()))
company_ticker = nifty_50_dict[company_name]
model_choice = st.sidebar.radio("Model", ["Random Forest", "XGBoost"])
period = st.sidebar.selectbox("Training history", ["1y", "2y", "5y"], index=1)

if st.sidebar.button("Train & Predict"):
    with st.spinner(f"Downloading {period} of data and training on {company_name}..."):
        df = yf.download(company_ticker, period=period, interval="1d", progress=False)
        df = df.droplevel(1, axis=1) if isinstance(df.columns, pd.MultiIndex) else df

        model_type = "xgboost" if model_choice == "XGBoost" else "random_forest"
        result = train_model(df, model_type=model_type)

        from model_trainer import save_model, load_model
        save_model(result, f"models/{company_ticker}_{model_type}.joblib")
        bundle = load_model(f"models/{company_ticker}_{model_type}.joblib")
        prediction, confidence = predict_next_direction(bundle, df)

    st.subheader("Prediction")
    p1, p2 = st.columns(2)
    with p1:
        st.metric("Next-Day Direction", prediction)
    with p2:
        st.metric("Model Confidence", f"{confidence:.1%}")

    if result.accuracy <= result.baseline_accuracy:
        st.warning(
            "This model did not clearly beat the majority-class baseline on the test set. "
            "Next-day price direction is a genuinely hard prediction problem — treat this "
            "as a directional signal, not financial advice."
        )

    st.divider()
    st.subheader("Model Performance (on held-out test period)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Accuracy", f"{result.accuracy:.1%}")
    m2.metric("Baseline Accuracy", f"{result.baseline_accuracy:.1%}")
    m3.metric("Precision", f"{result.precision:.1%}")
    m4.metric("Recall", f"{result.recall:.1%}")

    st.write("Confusion matrix (rows = actual, cols = predicted):")
    st.dataframe(
        pd.DataFrame(
            result.confusion,
            index=["Actual Down", "Actual Up"],
            columns=["Predicted Down", "Predicted Up"],
        )
    )

    st.divider()
    st.subheader("Top Predictive Features")
    st.bar_chart(result.feature_importance.head(15))

    st.divider()
    st.subheader("Recent Candlestick Chart")
    recent = df.tail(60)
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=recent.index,
                open=recent["Open"],
                high=recent["High"],
                low=recent["Low"],
                close=recent["Close"],
            )
        ]
    )
    fig.update_layout(xaxis_rangeslider_visible=False, height=450)
    st.plotly_chart(fig, use_container_width=True)

    patterns_found = detect_all_patterns(df).tail(1)
    active = [c.replace("pattern_", "") for c in patterns_found.columns if patterns_found[c].iloc[0] == 1]
    if active:
        st.write("Patterns detected on the most recent candle:", ", ".join(active))
    else:
        st.write("No named candlestick pattern detected on the most recent candle.")
else:
    st.info("Select a company and click **Train & Predict** in the sidebar to run the model.")
