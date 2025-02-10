import streamlit as st
import plotly.graph_objects as go
import pandas as pd

class HistoryPage():
    def __init__(self, df):
        
        fig_price = go.Figure(data=[go.Bar(x=df['Date'], y=df['Close'])])
        fig_price.update_layout(title='Brent Price Over Time in US')

        fig_price.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            xaxis_rangeslider_visible=True
        )

        col_button_cri_2008, col_button_cri_2014, col_button_cri_2020, col_button_high_2022 = st.columns(4)

        text = 'Click on the buttons to see what happened with Brent Price...'
        with col_button_cri_2008:
            if st.button('2008 Crisis'):
                fig_price.add_vrect(x0='2008-1-1', x1='2008-12-31', line_width=0, fillcolor="red", opacity=0.2)
                text = 'In the past, supply disruptions triggered by political events have caused oil prices to shift drastically; the Iranian revolution, Iran-Iraq war, Arab oil embargo, and Persian Gulf wars have been especially notable. The Asian financial crisis and the global economic crisis of 2007-2008 also caused fluctuation... the price run-up of 2007–08 was caused by strong demand confronting stagnating world production.'

        with col_button_cri_2014:
            if st.button('2014-2016 Crisis'):
                fig_price.add_vrect(x0='2014-1-1', x1='2016-12-31', line_width=0, fillcolor="red", opacity=0.2)
                text = "Between 2014 and 2016, global oil prices collapsed from over $100 per barrel to below $30 due to oversupply, especially from U.S. shale production, and OPEC's decision not to cut production. A slowdown in global demand, particularly from China, worsened the situation. This caused financial stress for oil-producing countries and companies, with many facing bankruptcies. In late 2016, OPEC and non-OPEC countries (OPEC+) agreed to cut production, leading to a gradual price recovery. By the end of 2016, prices started to stabilize above $50 per barrel."


        with col_button_cri_2020:
            if st.button('2020 Crisis'):
                fig_price.add_vrect(x0='2020-1-1', x1='2020-12-31', line_width=0, fillcolor="red", opacity=0.2)
                text = "The Brent Crude oil crisis of 2020 was driven by the COVID-19 pandemic, which drastically reduced global oil demand. In March, a price war between Saudi Arabia and Russia caused oil prices to plummet. By April, oil prices briefly dropped below $20 per barrel, and the WTI benchmark even went negative. In response, OPEC+ agreed to historic production cuts. Oil prices slowly recovered through the second half of 2020, but the market remained volatile."

        with col_button_high_2022:
            if st.button('2022 Rally'):
                fig_price.add_vrect(x0='2021-6-1', x1='2022-12-31', line_width=0, fillcolor="green", opacity=0.2)
                text = "In 2022, oil prices surged due to the Russia-Ukraine war, which disrupted global oil supplies and led to sanctions on Russian oil exports. Ongoing production cuts by OPEC+ and post-pandemic demand recovery also strained supply, pushing prices higher. Inflation and market speculation further contributed to the rally. By mid-year, Brent Crude prices hit around $120 per barrel. The combination of geopolitical tensions and supply-demand imbalances fueled the price increase."


        st.write(text)
        st.plotly_chart(fig_price)