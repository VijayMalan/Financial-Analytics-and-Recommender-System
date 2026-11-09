import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

beta_df = pd.read_csv("Betas")


st.title('Welcome to Company Overall Analysis.')
st.write('Here you will See all the important "Abouts" of the Company')
st.write('Just Select a Company and see the Magic Happen')
st.divider()

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


def company_id(ticker):
  company_name = yf.Ticker(ticker)
  return company_name.get_isin()


def company_overall_analysis(ticker):
    company = yf.Ticker(ticker)
    info_dict = company.get_info()
    

    # Basic details
    id = company_id(ticker)

    previous_close = info_dict.get('previousClose', 'N/A')
    market_cap = info_dict.get('marketCap', 'N/A')

    open_price = info_dict.get('open', 'N/A')
    CMP = info_dict.get('currentPrice', 'N/A')
    day_low = info_dict.get('dayLow', 'N/A')
    day_high = info_dict.get('dayHigh', 'N/A')
    fiftytwoweekhigh = info_dict.get('fiftyTwoWeekHigh', 'N/A')
    fiftytwoweeklow = info_dict.get('fiftyTwoWeekLow', 'N/A')

    # Location & Business
    Hq = info_dict.get('city', 'N/A')
    Country = info_dict.get('country', 'N/A')
    Website_url = info_dict.get('website', 'N/A')
    sector = info_dict.get('sector', 'N/A')
    full_name = info_dict.get('longName', 'N/A')
    business_summary = info_dict.get('longBusinessSummary', 'N/A')

    # Financials
    #beta = info_dict.get('beta', 'N/A')
    trailingPE = info_dict.get('trailingPE', 'N/A')
    Total_cash = info_dict.get('totalCash', 'N/A')
    total_cash_per_share = info_dict.get('totalCashPerShare', 'N/A')
    Ebitda = info_dict.get('ebitda', 'N/A')
    Debt = info_dict.get('totalDebt', 'N/A')
    quick_ratio = info_dict.get('quickRatio', 'N/A')
    current_ratio = info_dict.get('currentRatio', 'N/A')
    total_revenue = info_dict.get('totalRevenue', 'N/A')
    debt_to_equity = info_dict.get('debtToEquity', 'N/A')
    rps = info_dict.get('revenuePerShare', 'N/A')
    roa = info_dict.get('returnOnAssets', 'N/A')
    roe = info_dict.get('returnOnEquity', 'N/A')
    gross_profit = info_dict.get('grossProfits', 'N/A')
    fcf = info_dict.get('freeCashflow', 'N/A')
    ocf = info_dict.get('operatingCashflow', 'N/A')
    earnings_growth = info_dict.get('earningsGrowth', 'N/A')
    revenue_growth = info_dict.get('revenueGrowth', 'N/A')
    gross_margin = info_dict.get('grossMargins', 'N/A')
    ebitda_margin = info_dict.get('ebitdaMargins', 'N/A')
    operating_margin = info_dict.get('operatingMargins', 'N/A')
    dividend_rate = info_dict.get('dividendRate', 'N/A')
    dividend_yield = info_dict.get('dividendYield', 'N/A')
    payout_ratio = info_dict.get('payoutRatio', 'N/A')
    Book_value = info_dict.get('bookValue', 'N/A')
    Price_to_book = info_dict.get('priceToBook', 'N/A')



    st.subheader('BASIC DETAILS')
    st.divider()
    b1 , b2  = st.columns(2)

    with b1:
        st.metric('Current Market Price:' , CMP)
        st.metric('Opening Price:' , open_price)
        st.metric('Day High:' , day_high)
        st.metric('52 Week High:' , fiftytwoweekhigh)

    with b2:
        st.metric('Market Capitalization:' , market_cap)    
        st.metric('Previous Close:' , previous_close)
        st.metric('Day Low:' , day_low)
        st.metric('52 Week Low:' , fiftytwoweeklow)

    st.divider()
    st.subheader('FINANCIAL OVERVIEW')
    st.divider()
    col1 , col2 , col3 = st.columns(3)
    
    with col1:
        st.metric('P/E Ratio:' , trailingPE)
        st.metric('Current Ratio:' , current_ratio)
        st.metric('Current Debt:' , Debt)
        st.metric('Book Value:' , Book_value)
        st.metric('Gross Margin:' , gross_margin)
        st.metric('Return Per Share:' , rps)
        st.metric('Total Revenue:' , total_revenue)
        st.metric('Free Cash Flow:' , fcf)




    with col2:
        st.metric('P/B Ratio:' , Price_to_book)
        st.metric('Quick Ratio:' , quick_ratio)
        st.metric('Total Cash:' , Total_cash)
        st.metric('PayOut Ratio:' , payout_ratio)
        st.metric('EBITDA Margin:' , ebitda_margin)
        st.metric('Return on Equity:' , roe)
        st.metric('Debt To Equity Ratio:' , debt_to_equity)
        st.metric('Operating Cash Flow:' , ocf)



    with col3:
        st.metric('Dividend Rate:' , dividend_rate)
        st.metric('EBITDA:' , Ebitda)
        st.metric('Total Cash Per Share:' , total_cash_per_share)
        st.metric('Dividend Yield:' , dividend_yield)
        st.metric('Operating Margin:' , operating_margin)
        st.metric('Return on Assets:' , roa)
        st.metric('Gross Profit:' , gross_profit)
        st.metric('Revenue Growth:' , revenue_growth)


    st.divider()  

    st.subheader('LOCATION AND BUSINESS')
    st.divider()
    a1 , a2 , a3 = st.columns(3)

    with a1:
        st.metric('Company Name:' , full_name)

    with a2:
        st.metric('Sector:' , sector)    

    with a3:
        st.metric('HeadQuarters:' , Hq)

    st.metric('Website:' , Website_url)
    st.write('Business Summary:' , business_summary)  
    st.divider()
      





company_overall_analysis(company_ticker)   

   



