import streamlit as st
import pandas as pd


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
    company_ticker = company_name
elif index_name == 'NIFTY NEXT 50':
    company_name = st.sidebar.selectbox(
    "Please Select a Company",
    list(nifty_next_50_dict.keys())
    )
    company_ticker = company_name
elif index_name == 'NIFTY MIDCAP 50':
    company_name = st.sidebar.selectbox(
    "Please Select a Company",
    list(nifty_midcap_50_dict.keys())
    )
    company_ticker = company_name
elif index_name == 'NIFTY SMALLCAP 50':
    company_name = st.sidebar.selectbox(
    "Please Select a Company",
    list(nifty_smallcap_50_dict.keys())
    )
    company_ticker = company_name

st.title("Recommender System")
st.write("Here you will get to know similar companies to your selected companies.")

df = pd.read_csv('Recommender_system.csv')

df.drop(columns = ['Unnamed: 0'] , inplace = True)

# Make a copy just to be safe
df_numeric = df.copy()

# Step 1: Set 'Company' column aside
company_names = df_numeric['Company']

# Step 2: Work only on numeric columns
numeric_df = df_numeric.drop(columns=['Company'])

# Step 3: Fill NaNs with column-wise means
numeric_filled = numeric_df.fillna(numeric_df.mean())

# Step 4: Add 'Company' column back
df_cleaned = pd.concat([company_names, numeric_filled], axis=1)

from sklearn.preprocessing import MinMaxScaler

# Select only numeric features (excluding 'Company')
features = df_cleaned.columns[1:]  # All columns except 'Company'
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df_cleaned[features])

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=7, random_state=42)
clusters = kmeans.fit_predict(scaled_data)

# Add clusters to your cleaned DataFrame
df_cleaned['Cluster'] = clusters

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler


feature_cols = df_cleaned.columns[1:]  

# Normalize the data
scaler = MinMaxScaler()
normalized_features = scaler.fit_transform(df_cleaned[feature_cols])

ohe_df_normalized = pd.DataFrame(normalized_features, columns=feature_cols, index=df_cleaned["Company"])
cosine_sim_matrix = cosine_similarity(ohe_df_normalized)

def cosine_recommender(company_name, top_n=5):
   
    if company_name not in ohe_df_normalized.index:
        raise ValueError("Company not found in the dataset.")

    idx = ohe_df_normalized.index.get_loc(company_name)
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]

    recommended_indices = [i[0] for i in sim_scores]
    similarity_scores = [i[1] for i in sim_scores]

    
    result_df = pd.DataFrame({
        "Company": ohe_df_normalized.index[recommended_indices],
        "Similarity Score": similarity_scores
    })

    return result_df
recommender_df = cosine_recommender(company_ticker)

st.dataframe(recommender_df)