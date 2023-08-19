from tastytrade import Account
import pandas as pd
import streamlit as st
from datetime import time
import pytz

PAGE_TITLE = "Net Liq"
PAGE_ICON = "📈"
TIME_PERIOD_OPTIONS = ["1d", "1m", "3m", "6m", "1y", "all"]

def main():
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

    st.title(PAGE_TITLE)

    account = st.session_state.tt_account
    session = st.session_state.tt_session

    if 'time_back' not in st.session_state:
        st.session_state.time_back = None
    
    current_time_back = st.sidebar.selectbox("Timeperiod", TIME_PERIOD_OPTIONS, index=2)
    if st.session_state.time_back != current_time_back:
        st.session_state.time_back = current_time_back
        netliqs = get_net_liq(account, session, st.session_state.time_back)
    else:
        netliqs = get_net_liq(account, session, st.session_state.time_back)

    st.write(f"Timeperiod: {st.session_state.time_back}")

    chart_data = get_net_liq_chart_data(netliqs)
    
    st.line_chart(chart_data['Net Liquidating Value'])

def get_net_liq(account, session, time_back):
    return Account.get_net_liquidating_value_history(account, session, time_back)

# Still need to get the correct time, closest to the SPY close time from yahoo finance.
# Little too much AI on this one, lost track of what was going on
def get_net_liq_chart_data(netliqs):
    data = []
  
    for netliq in netliqs:
        data.append({
            "time": netliq.time,
            "Net Liquidating Value": float(netliq.total_close)
        })

    data = pd.DataFrame(data)

    data['date'] = data['time'].dt.date

    # Group by date and keep only the record with the smallest time difference from 8:00 UTC
    data = data.loc[data.reset_index().groupby('date')['time'].idxmin()]

    data.set_index("time", inplace=True)

    return data

if __name__ == "__main__":
    main()
