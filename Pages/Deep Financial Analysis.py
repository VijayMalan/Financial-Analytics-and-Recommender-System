import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


balance_sheet_metrics_dict = {

    'Net Debt' : 'NetDebt',
    'Total Debt' : 'TotalDebt',
    'Working Capital' : 'WorkingCapital',
    'Net Tangible Assets' : 'NetTangibleAssets',
    'Other Intangible Assets' : 'OtherIntangibleAssets',
    'Market Capitalization' : 'TotalCapitalization',
    'StockHolders Equity' : 'StockholdersEquity',
    'Other Equity Interest' : 'OtherEquityInterest',
    'Total Liabilities Net Minority Interest' : 'TotalLiabilitiesNetMinorityInterest',
    'Total Non Current Liabilities Net Minority Interest' : 'TotalNonCurrentLiabilitiesNetMinorityInterest',
    'Other Non Current Liabilities' : 'OtherNonCurrentLiabilities',
    'Long Term Debt and Capital Lease Obligation' : 'LongTermDebtAndCapitalLeaseObligation',
    'Current Liabilities' : 'CurrentLiabilities',
    'Other Current Liabilities' : 'OtherCurrentLiabilities',
    'Current Debt and Capital Lease Obligation' : 'CurrentDebtAndCapitalLeaseObligation',
    'Dividends Payable' : 'DividendsPayable',
    'Total Assets' : 'TotalAssets',
    'Total Non Current Assets' : 'TotalNonCurrentAssets',
    'Investment in Financial Assets' : 'InvestmentinFinancialAssets',
    'Available for Sales Securities' : 'AvailableForSaleSecurities',
    'Financial Assets Designated as Fair Value Through Profit or Loss Total' : 'FinancialAssetsDesignatedasFairValueThroughProfitorLossTotal',
    'Long Term Equity Investment' : 'LongTermEquityInvestment',
    'Investments in Joint Ventures at Cost' : 'InvestmentsinJointVenturesatCost',
    'Investments in Associates at Cost' : 'InvestmentsinAssociatesatCost',
    'Goodwill' : 'Goodwill',
    'Net PPE' : 'NetPPE',
    'Gross PPE' : 'GrossPPE',
    'Accumulated Depreciation' : 'AccumulatedDepreciation'

}

income_statement_metrics_dict = {
    'Normalized EBITDA' : 'NormalizedEBITDA',
    'Total Unusual Items' : 'TotalUnusualItems',
    'NetIncome From Continuing Operation Net Minority Interest' : 'NetIncomeFromContinuingOperationNetMinorityInterest',
    'EBITDA' : 'EBITDA',
    'EBIT' : 'EBIT',
    'Net Interest Income' : 'NetInterestIncome',
    'Interest Expense' : 'InterestExpense',
    'Interest Income' : 'InterestIncome',
    'Normalized Income' : 'NormalizedIncome',
    'Total Expenses' : 'TotalExpenses',
    'Diluted EPS' : 'DilutedEPS',
    'Basic EPS' : 'BasicEPS',
    'Net Income' : 'NetIncome',
    'Net Income Continuous Operations' : 'NetIncomeContinuousOperations',
    'Pre-tax Income' : 'PretaxIncome',
    'Total Other Finance Cost' : 'TotalOtherFinanceCost',
    'Operating Income' : 'OperatingIncome',
    'Operating Expense' : 'OperatingExpense',
    'Other Operating Expenses' : 'OtherOperatingExpenses',
    'Selling General And Administration' : 'SellingGeneralAndAdministration',
    'Selling and Marketing Expense' : 'SellingAndMarketingExpense',
    'General and Administrative Expense' : 'GeneralAndAdministrativeExpense',
    'Rent and Landing Fees' : 'RentAndLandingFees',
    'Gross Profit' : 'GrossProfit',
    'Cost of Revenue' : 'CostOfRevenue',
    'Total Revenue' : 'TotalRevenue'
}

cash_flow_statement_dict = {
    'Free Cash Flow' : 'FreeCashFlow',
    'Capital Expenditure' : 'CapitalExpenditure',
    'Changes In Cash' : 'ChangesInCash',
    'Financing Cash Flow' : 'FinancingCashFlow',
    'Cash Dividends Paid' : 'CashDividendsPaid',
    'InvestingCashFlow' : 'InvestingCashFlow',
    'Operating Cash Flow' : 'OperatingCashFlow',
    'Change in Working Capital' : 'ChangeInWorkingCapital',
    'NetForeignCurrencyExchangeGainLoss' : 'NetForeignCurrencyExchangeGainLoss',
    'NetIncomeFromContinuingOperations' : 'NetIncomeFromContinuingOperations'
}

nifty_50_dict = {
    'Adani Enterprises': 'ADANIENT.NS',
    'Adani Ports': 'ADANIPORTS.NS',
    'Apollo Hospital': 'APOLLOHOSP.NS',
    'Asian Paints': 'ASIANPAINT.NS',
    'Axis Bank': 'AXISBANK.NS',
    'Bajaj Auto': 'BAJAJ-AUTO.NS',
    'Bajaj Finance': 'BAJFINANCE.NS',
    'Bajaj Finserv': 'BAJAJFINSV.NS',
    'Bharat Electric': 'BEL.NS',
    'Bharti Airtel': 'BHARTIARTL.NS',
    'Cipla': 'CIPLA.NS',
    'Coal India': 'COALINDIA.NS',
    'Dr Reddys Labs': 'DRREDDY.NS',
    'Eicher Motors': 'EICHERMOT.NS',
    'Eternal': 'EPL.NS',
    'Grasim': 'GRASIM.NS',
    'HCL Tech': 'HCLTECH.NS',
    'HDFC Bank': 'HDFCBANK.NS',
    'HDFC Life': 'HDFCLIFE.NS',
    'HUL': 'HINDUNILVR.NS',
    'Hero MotoCorporation': 'HEROMOTOCO.NS',
    'Hindalco': 'HINDALCO.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    'ITC': 'ITC.NS',
    'IndusInd Bank': 'INDUSINDBK.NS',
    'Infosys': 'INFY.NS',
    'JSW Steel': 'JSWSTEEL.NS',
    'Jio Financial': 'JIOFIN.NS',
    'Kotak Mahindra': 'KOTAKBANK.NS',
    'Larsen': 'LT.NS',
    'M&M': 'M&M.NS',
    'Maruti Suzuki': 'MARUTI.NS',
    'NTPC': 'NTPC.NS',
    'Nestle': 'NESTLEIND.NS',
    'ONGC': 'ONGC.NS',
    'Power Grid Corporation': 'POWERGRID.NS',
    'Reliance': 'RELIANCE.NS',
    'SBI': 'SBIN.NS',
    'SBI Life Insurance': 'SBILIFE.NS',
    'Shriram Finance': 'SHRIRAMFIN.NS',
    'Sun Pharma': 'SUNPHARMA.NS',
    'TCS': 'TCS.NS',
    'Tata Cons. Prod': 'TATACONSUM.NS',
    'Tata Motors': 'TATAMOTORS.NS',
    'Tata Steel': 'TATASTEEL.NS',
    'Tech Mahindra': 'TECHM.NS',
    'Titan Company': 'TITAN.NS',
    'Trent': 'TRENT.NS',
    'Ultratech Cement': 'ULTRACEMCO.NS',
    'Wipro': 'WIPRO.NS',

}

nifty_midcap_50_dict = {
    'Alkem Lab': 'ALKEM.NS',
    'Ashok Leyland': 'ASHOKLEY.NS',
    'Astral Ltd': 'ASTRAL.NS',
    'AU Small Finance': 'AUBANK.NS',
    'Aurobindo Pharma': 'AUROPHARMA.NS',
    'Bharat Forge': 'BHARATFORG.NS',
    'BHEL': 'BHEL.NS',
    'BSE Limited': 'BSE.NS',
    'Colgate': 'COLPAL.NS',
    'Co Forge Ltd': 'COFORGE.NS',
    'Container Corporation': 'CONCOR.NS',
    'Cummins': 'CUMMINSIND.NS',
    'Dixon Technology': 'DIXON.NS',
    'Federal Bank': 'FEDERALBNK.NS',
    'GMR Airports': 'GMRINFRA.NS',
    'Godrej Prop': 'GODREJPROP.NS',
    'HDFC AMC': 'HDFCAMC.NS',
    'HINDPETRO': 'HINDPETRO.NS',
    'IDFC First Bank': 'IDFCFIRSTB.NS',
    'Indus Towers': 'INDUSTOWER.NS',
    'IRCTC': 'IRCTC.NS',
    'Lupin': 'LUPIN.NS',
    'Marico': 'MARICO.NS',
    'Max Healthcare': 'MAXHEALTH.NS',
    'Mphasis': 'MPHASIS.NS',
    'MRF': 'MRF.NS',
    'Muthoot Finance': 'MUTHOOTFIN.NS',
    'NHPC': 'NHPC.NS',
    'NMDC': 'NMDC.NS',
    'Oberoi Realty': 'OBEROIRLTY.NS',
    'Oil India': 'OIL.NS',
    'Oracle': 'ORACLEFIN.NS',
    'Page Industries': 'PAGEIND.NS',
    'PB Fintech': 'POLICYBZR.NS',
    'Paytm': 'PAYTM.NS',
    'Persistent': 'PERSISTENT.NS',
    'Petronet LNG': 'PETRONET.NS',
    'Phoenix Mills': 'PHOENIXLTD.NS',
    'PI Industries': 'PIIND.NS',
    'Polycab': 'POLYCAB.NS',
    'Prestige Estate': 'PRESTIGE.NS',
    'SAIL': 'SAIL.NS',
    'SBI Card': 'SBICARD.NS',
    'SRF': 'SRF.NS',
    'Supreme Ind': 'SUPREMEIND.NS',
    'Torrent Power': 'TORNTPOWER.NS',
    'Tube Investment': 'TIINDIA.NS',
    'Voltas': 'VOLTAS.NS',
    'Vodafone Idea': 'IDEA.NS',
    'Yes Bank': 'YESBANK.NS'

}

nifty_smallcap_50_dict = {
    'AFFLE 3I': 'AFFLE.NS',
    'Aarti Ind': 'AARTIIND.NS',
    'Aditya Birla Re': 'ADANIRENEW.NS',
    'Aegis Logistics': 'AEGISCHEM.NS',
    'Amara Raja': 'AMARAJABAT.NS',
    'Amber Enterprises': 'AMBER.NS',
    'Angel One': 'ANGELONE.NS',
    'Aster DM Health': 'ASTERDM.NS',
    'BirlaSoft': 'BSOFT.NS',
    'Brigade Enterprises': 'BRIGADE.NS',
    'CAMS': 'CAMS.NS',
    'CDSL': 'CDSL.NS',
    'CESC': 'CESC.NS',
    'CG Consumer': 'CROMPTON.NS',
    'Castrol': 'CASTROLIND.NS',
    'Cyient': 'CYIENT.NS',
    'Delhivery': 'DELHIVERY.NS',
    'Dr Lal PathLab': 'LALPATHLAB.NS',
    'FirstSource Sol': 'FSL.NS',
    'Five-Star Busin': 'FIVESTAR.NS',
    'GE Shipping': 'GESHIP.NS',
    'Guj State Petro': 'GSPL.NS',
    'HFCL': 'HFCL.NS',
    'Himadri Special': 'HSCL.NS',
    'Hind Copper': 'HINDCOPPER.NS',
    'IEX': 'IEX.NS',
    'IIFL Finance': 'IIFL.NS',
    'Inox Wind': 'INOXWIND.NS',
    'KEC International': 'KEC.NS',
    'Kaynes Tech': 'KAYNES.NS',
    'Kfin Tech': 'KFINTECH.NS',
    'Laurus Labs': 'LAURUSLABS.NS',
    'MCX India': 'MCX.NS',
    'NBCC(India)': 'NBCC.NS',
    'NCC': 'NCC.NS',
    'Natco Pharma': 'NATCOPHARM.NS',
    'Navin Fluorine': 'NAVINFLUOR.NS',
    'Neuland Lab': 'NEULANDLAB.NS',
    'PNB Housing Finance': 'PNBHOUSING.NS',
    'Piramal Pharma': 'PIRAMALPH.NS',
    'Piramal Enterprises': 'PEL.NS',
    'Poonawalla Finance': 'POONAWALLAFIN.NS',
    'Radico Khaitan': 'RADICO.NS',
    'RamKrishnaForge': 'RKFORGE.NS',
    'Ramco Cements': 'RAMCOCEM.NS',
    'Reliance Power': 'RPOWER.NS',
    'Sonata': 'SONATSOFTW.NS',
    'Tata Chemicals': 'TATACHEM.NS',
    'Tejas Networks': 'TEJASNET.NS',
    'Zensar Tech': 'ZENSARTECH.NS',

}


nifty_next_50_dict = {
    'ABB India': 'ABB.NS',
    'Adani Energy': 'ADANIENSOL.NS',
    'Adani Green Energies': 'ADANIGREEN.NS',
    'Adani Power': 'ADANIPOWER.NS',
    'Ambuja Cements': 'AMBUJACEM.NS',
    'Avenue Supermarkets': 'DMART.NS',
    'BPCL': 'BPCL.NS',
    'Bajaj Holdings': 'BAJAJHLDNG.NS',
    'Bank of Baroda': 'BANKBARODA.NS',
    'Biocon': 'BIOCON.NS',
    'Bombay Dyeing': 'BOMDYEING.NS',
    'Bosch': 'BOSCHLTD.NS',
    'Britannia': 'BRITANNIA.NS',
    'CG Power': 'CGPOWER.NS',
    'Canara Bank': 'CANBK.NS',
    'Chola Investments': 'CHOLAFIN.NS',
    'Dabur India': 'DABUR.NS',
    'DLF': 'DLF.NS',
    'Divis Labs': 'DIVISLAB.NS',
    'GAIL': 'GAIL.NS',
    'Godrej Consumer': 'GODREJCP.NS',
    'Havells India': 'HAVELLS.NS',
    'Hindustan Aeronauticals': 'HAL.NS',
    'ICICI Lombard': 'ICICIGI.NS',
    'ICICI Prudentials': 'ICICIPRULI.NS',
    'IOC': 'IOC.NS',
    'IRFC': 'IRFC.NS',
    'Indian Hotels': 'INDHOTEL.NS',
    'Info Edge': 'NAUKRI.NS',
    'InterGlobe Aviation': 'INDIGO.NS',
    'Jindal Steel': 'JINDALSTEL.NS',
    'JSW Energy': 'JSWENERGY.NS',
    'LIC India': 'LICI.NS',
    'LTMind Tree': 'LTIM.NS',
    'Macrotech Dev': 'LODHA.NS',
    'Mother Son': 'MOTHERSON.NS',
    'PNB': 'PNB.NS',
    'PVR INOX': 'PVRINOX.NS',
    'Pidilite Ind': 'PIDILITIND.NS',
    'Power Finance': 'PFC.NS',
    'REC': 'RECLTD.NS',
    'Shree Cements': 'SHREECEM.NS',
    'Siemens': 'SIEMENS.NS',
    'TVS Motors': 'TVSMOTOR.NS',
    'Tata Power': 'TATAPOWER.NS',
    'Torrent Pharma': 'TORNTPHARM.NS',
    'UNited Spirits': 'MCDOWELL-N.NS',
    'Vedanta': 'VEDL.NS',
    'Varun Beverages': 'VBL.NS',
    'Zydus Life': 'ZYDUSLIFE.NS'
}

index_name = st.sidebar.selectbox(
    "Please Select a Index" , 
    ['NIFTY 50' , 'NIFTY NEXT 50' , 'NIFTY MIDCAP 50' , 'NIFTY SMALLCAP 50']
)

if index_name == 'NIFTY 50':
    company_name = st.sidebar.selectbox(
    "Please Select a Company",
    list(nifty_50_dict.keys())
    )
    company_ticker = nifty_50_dict[company_name]
elif index_name == 'NIFTY NEXT 50':
    company_name = st.sidebar.selectbox(
    "Please Select a Company",
    list(nifty_next_50_dict.keys())
    )
    company_ticker = nifty_next_50_dict[company_name]
elif index_name == 'NIFTY MIDCAP 50':
    company_name = st.sidebar.selectbox(
    "Please Select a Company",
    list(nifty_midcap_50_dict.keys())
    )
    company_ticker = nifty_midcap_50_dict[company_name]
elif index_name == 'NIFTY SMALLCAP 50':
    company_name = st.sidebar.selectbox(
    "Please Select a Company",
    list(nifty_smallcap_50_dict.keys())
    )
    company_ticker = nifty_smallcap_50_dict[company_name]

# Balance sheet dataframe
def fetch_balance_sheet_metrics(company_ticker, metric_name_in_dict):

    metric_name_in_balance_sheet = balance_sheet_metrics_dict[metric_name_in_dict]

    company = yf.Ticker(company_ticker)
    balance_sheet_df = company.get_balance_sheet()
    balance_sheet_df = balance_sheet_df.reset_index()

    balance_sheet_df.columns = (['Metrics' , '31-3-2025' , '31-3-2024' , '31-3-2023' , '31-3-2022' , '6'])
    balance_sheet_df.drop(columns = ['6'] , inplace = True)

    return balance_sheet_df.loc[balance_sheet_df['Metrics'] == metric_name_in_balance_sheet]

# Income sheet dataframe

def fetch_income_statement_metrics(company_ticker, metric_name_in_dict):

    metric_name_in_income_stmt = income_statement_metrics_dict[metric_name_in_dict]

    company = yf.Ticker(company_ticker)
    income_stmt_df = company.get_income_stmt()
    income_stmt_df = income_stmt_df.reset_index()

    income_stmt_df.columns = (['Metrics' , '31-3-2025' , '31-3-2024' , '31-3-2023' , '31-3-2022' , '6'])
    income_stmt_df.drop(columns = ['6'] , inplace = True)

    return income_stmt_df.loc[income_stmt_df['Metrics'] == metric_name_in_income_stmt]

# Cash Flow Metrics Dataframe
def fetch_cash_flow_metrics(company_ticker, metric_name_in_dict):

    metric_name_in_cash_flow = cash_flow_statement_dict[metric_name_in_dict]

    company = yf.Ticker(company_ticker)
    cash_flow_df = company.get_cash_flow()
    cash_flow_df = cash_flow_df.reset_index()

    cash_flow_df.columns = (['Metrics' , '31-3-2025' , '31-3-2024' , '31-3-2023' , '31-3-2022' , '6'])
    cash_flow_df.drop(columns = ['6'] , inplace = True)

    return cash_flow_df.loc[cash_flow_df['Metrics'] == metric_name_in_cash_flow]

# Dividends Stocksplits

def Dividends_StockSplits(ticker):
  company_name = yf.Ticker(ticker)
  return company_name.get_actions(period = 'max')

# Share Holdings pie chart

def Share_Holdings(ticker):
    company_name = yf.Ticker(ticker)
    share_holding_df = company_name.get_major_holders()

    number = share_holding_df.loc['institutionsCount', 'Value']

    only_percentages_df = share_holding_df.drop(['institutionsCount', 'institutionsFloatPercentHeld'] , axis=0)

    public_val = 1 - only_percentages_df.loc['insidersPercentHeld', 'Value'] - only_percentages_df.loc['institutionsPercentHeld', 'Value']

    only_percentages_df.loc['Publically Available'] = public_val

    labels = ['Promoter Holdings', 'Other Institutions', 'Publically Available']
    explode = (0.05, 0.05, 0)

    plt.figure(figsize=(3, 3))
    plt.pie(
        only_percentages_df['Value'],
        labels=labels,
        explode=explode,
        shadow=True,
        autopct='%1.1f%%',
        startangle=90
    )

    plt.text(-1.5, -1.2, f"Number of Institutions : {int(number)}", ha='center', va='center', fontsize=8, color='black')
    plt.title('Share Holding Distribution', y=1.00)
    plt.axis('equal')
    plt.show()


# EPS Records
nifty_companies = {

}
def EPS_records(ticker):
    value_to_find = ticker
    key = next((k for k, v in nifty_companies.items() if v == value_to_find), None)

    company_name = yf.Ticker(ticker)
    eps_df = company_name.get_earnings_dates()
    eps_df.index = pd.to_datetime(eps_df.index)

    eps_df['Formatted Date'] = eps_df.index.strftime('%B %Y')

    plt.figure(figsize=(10, 5))
    plt.plot(eps_df['Formatted Date'], eps_df['EPS Estimate'], marker='o', label='EPS Estimate', color='royalblue')
    plt.plot(eps_df['Formatted Date'], eps_df['Reported EPS'], marker='s', label='Reported EPS', color='darkorange')

    plt.xticks(rotation=45)
    plt.title(f"Estimated EPS vs Reported EPS for {key}")
    plt.xlabel("Earnings Date")
    plt.ylabel("EPS")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Price Estimates Dataframe

def price_estimates(ticker):
  company_name = yf.Ticker(ticker)
  return company_name.get_analyst_price_targets()



st.divider()
st.subheader("Metric Explorer")

statement_type = st.sidebar.selectbox(
    "Select a Statement",
    ["Balance Sheet", "Income Statement", "Cash Flow"]
)

if statement_type == "Balance Sheet":
    metric_name = st.sidebar.selectbox(
        "Select a Metric",
        list(balance_sheet_metrics_dict.keys())
    )
    result_df = fetch_balance_sheet_metrics(company_ticker, metric_name)

elif statement_type == "Income Statement":
    metric_name = st.sidebar.selectbox(
        "Select a Metric",
        list(income_statement_metrics_dict.keys())
    )
    result_df = fetch_income_statement_metrics(company_ticker, metric_name)

else:  # Cash Flow
    metric_name = st.sidebar.selectbox(
        "Select a Metric",
        list(cash_flow_statement_dict.keys())
    )
    result_df = fetch_cash_flow_metrics(company_ticker, metric_name)

if result_df.empty:
    st.warning(f"No data found for '{metric_name}' on {company_ticker}. "
               "This metric may not be reported for this company.")
else:
    st.dataframe(result_df, use_container_width=True)