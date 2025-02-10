import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler

class HomePage():
    def __init__(self, df):
        

        def custom_legend_name(fig, new_names):
            for i, new_name in enumerate(new_names):
                fig.data[i].name = new_name

        @st.cache_data()        
        def get_date():
            start_date = pd.to_datetime(df.Date).min().timestamp()
            end_date = pd.to_datetime(df.Date).max().timestamp()

            start_date = datetime.fromtimestamp(start_date)
            end_date = datetime.fromtimestamp(end_date)

            return start_date, end_date

        start_date, end_date = get_date()
        selected_date_range = st.slider(
            "Select a date range",
            min_value=start_date,
            max_value=end_date,
            value=(start_date, end_date),
            step=timedelta(days=1),
        )
        start = datetime.date(selected_date_range[0])
        end = datetime.date(selected_date_range[1])

        period_col, col_ma_sd = st.columns(2)

        with period_col:
            option_per = st.selectbox("Period:", ['Daily', "Weekly", 'Monthly', 'Yearly'])
        
        with col_ma_sd:
            option_ma_sd = st.selectbox("MA and SD::", ['None', 'MA20', "MA50", 'SD'])

        
        df = df.loc[start:end]

        if option_per == 'Daily':
            ...

        if option_per == 'Yearly':
            df = df.groupby('year').agg({
                'Open': 'first',    # First open price of the year
                'Close': 'last',    # Last close price of the year
                'High': 'max',      # Maximum high price of the year
                'Low': 'min',       # Minimum low price of the year
                'Volume': 'sum'     # Total volume traded in the year
            }).reset_index()

            df['Date'] = df['year']
        
        if option_per == 'Monthly':
            df['per'] = df.Date.dt.to_period("M")

            df = df.groupby('per').agg({
                'Open': 'first',    # First open price of the year
                'Close': 'last',    # Last close price of the year
                'High': 'max',      # Maximum high price of the year
                'Low': 'min',       # Minimum low price of the year
                'Volume': 'sum'     # Total volume traded in the year
            }).reset_index()

            df['Date'] = df.per.dt.strftime("%Y-%m")

        if option_per == 'Weekly':
            df['Date'] = pd.to_datetime(df['Date']) - pd.to_timedelta(7, unit='d')
            df = df.groupby([pd.Grouper(key='Date', freq='W-MON')]).agg({
                'Open': 'first',    # First open price of the year
                'Close': 'last',    # Last close price of the year
                'High': 'max',      # Maximum high price of the year
                'Low': 'min',       # Minimum low price of the year
                'Volume': 'sum'     # Total volume traded in the year
            }).reset_index()


        fig_price = go.Figure(data=[go.Candlestick(x=df['Date'],
                                            open=df['Open'],
                                            high=df['High'],
                                            low=df['Low'],
                                            close=df['Close'])])
        fig_price.update_layout(title='Brent Price Over Time in USD')

        fig_volume = go.Figure(data=[go.Bar(x=df['Date'], y=df['Volume'])])
        fig_volume.update_layout(title='Brent Volume Over Time in US')

        fig_volume.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            xaxis_rangeslider_visible=True
        )

        if "MA" in option_ma_sd:

            num = int(option_ma_sd[2:])
            df[f'MA{num}'] = df.Close.rolling(num).mean()
                
            fig_price = go.Figure(data=[go.Candlestick(x=df['Date'],
                                        open=df['Open'],
                                        high=df['High'],
                                        low=df['Low'],
                                        close=df['Close']),
                                        go.Scatter(x=df.Date, y=df[f'MA{num}'], line=dict(color='purple', width=3))])
            fig_price.update_layout(title='Brent Price Over Time in USD')
            custom_legend_name(fig_price, ['Price',f'MA{num}'])
            fig_price.update_layout(legend=dict(yanchor="top", y=0.9, xanchor="right", x=0.9))
        

        if option_ma_sd == "SD":
            df['rolling_sd_value'] = df.Close.rolling(window=3).std()
            df['volume_sd'] = df.Volume.rolling(window=3).std()
                
            fig_price = go.Figure(data=[go.Scatter(x=df.Date, y=df['rolling_sd_value'], line=dict(color='purple', width=3))])
            fig_price.update_layout(title='Brent Price Deviation Over Time in USD')

            fig_volume = go.Figure(data=[go.Scatter(x=df.Date, y=df['volume_sd'], line=dict(color='orange', width=3))])
            fig_volume.update_layout(title='Brent Volume Deviation Over Time in US')
        


        col_price, col_volume = st.columns(2)
        
        with col_price:
            st.plotly_chart(fig_price)

        with col_volume:
            st.plotly_chart(fig_volume)