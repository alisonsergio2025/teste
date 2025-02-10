import streamlit as st
import warnings
from pandas.errors import SettingWithCopyWarning
from home import HomePage
from model import ModelPage
from history import HistoryPage
from forecast_class import Forecast

st.set_page_config(
    page_title="Brent Price Analysis",
    layout="wide"
)
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.simplefilter(action="ignore", category=UserWarning)
warnings.simplefilter(action="ignore")


@st.cache_data()
def create_model():
    brent = Forecast('BZ=F')
    brent.split_train_test()
    brent.train_xgb()

    return brent

brent = create_model()

st.write('# Brent Price Analysis')

tab = st.sidebar.radio("Pages:", ["Home", "Model", "History", "Prediction"])


if tab == 'Home':
    home_page = HomePage(brent.df)

if tab == 'Model':
    ModelPage(brent.metrics_xgb, brent.xbg_train_df, brent.xgb_test_df)

if tab == 'History':
    HistoryPage(brent.df)
