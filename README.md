# Financial Analytics & Stock Recommender System

An interactive stock market analytics dashboard built with Python and Streamlit. The application combines financial data analysis, machine learning-based stock movement prediction, and stock similarity recommendations.

## Features

### 1. Company Financial Analysis
- Explore financial information for individual companies.
- View key financial metrics and company information.
- Retrieve market data using Yahoo Finance.

### 2. Stock Movement Prediction
- Predict the next day's stock price direction (UP or DOWN).
- Supports Random Forest and XGBoost classification models.
- Uses historical stock data and engineered technical indicators.
- Displays model evaluation metrics and feature importance.

### 3. Stock Recommender System
- Identify stocks with similar characteristics.
- Uses K-Means clustering to group stocks.
- Uses cosine similarity to find comparable companies.
- Displays the top five similar stocks.

### 4. Interactive Dashboard
- Built using Streamlit.
- Includes interactive financial charts and visualizations.
- Uses Plotly and Matplotlib for data visualization.

## Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Dashboard | Streamlit |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Plotly |
| Financial Data | Yahoo Finance (yfinance) |
| Machine Learning | Scikit-learn, XGBoost |
| Similarity Analysis | K-Means, Cosine Similarity |

## Project Structure

```text
Financial-Analytics-and-Recommender-System/
│
├── Home.py
├── Pages/
│   ├── Company Overall Analysis.py
│   ├── Deep Financial Analysis.py
│   ├── Movement_Prediction.py
│   └── Recommender System.py
│
├── feature_engineering.py
├── model_trainer.py
├── candlestick_patterns.py
├── Recommender_system.csv
├── Betas
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/VijayMalan/Financial-Analytics-and-Recommender-System.git
cd Financial-Analytics-and-Recommender-System
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install streamlit pandas numpy matplotlib plotly yfinance scikit-learn xgboost joblib
```

### 4. Run the application

```bash
python -m streamlit run Home.py
```

The dashboard should open in your browser.

## Disclaimer

Stock movement predictions and similarity results are intended for educational and analytical purposes only. They should not be considered financial advice or recommendations to buy or sell securities.

## Attribution

This repository is based on and adapted from an existing project. Original-source attribution and permission should be maintained in accordance with the original author's terms.
