from tastytrade import Account, ProductionSession
import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, date

load_dotenv()

today = date.today()
first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)

default_values = {
    'tt_account': None,
    'sandbox': os.getenv('SANDBOX', 'False').lower() in ['true', '1'],
    'tt_session': None,
    'start_date': first_day_last_month,
    'end_date': today
}

for key, default_value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

st.set_page_config(page_title="tastyreports", page_icon="📈")

def login(username, password, sandbox):
    st.session_state.sandbox = sandbox
    session = ProductionSession(username, password)
    st.session_state.tt_session = session
    account = Account.get_accounts(st.session_state.tt_session)[0]
    st.session_state.tt_account = account

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

username = os.getenv('TT_USERNAME', '')
password = os.getenv('TT_PASSWORD', '')

if (username and password and not st.session_state['tt_session']):
    login(username, password, st.session_state.sandbox)

if (not st.session_state['tt_session']):
    st.title("Login")
    form_username = st.text_input('Username', value=username)
    form_password = st.text_input('Password', type='password', value=password)
    sandbox = False

    st.button('Login', on_click=login, args=[form_username, form_password, sandbox])
else:
    st.title("tastyreports")
    st.subheader('Settings')

    accounts = Account.get_accounts(st.session_state.tt_session)
    account_options = {f"{account.account_number} - {account.nickname}": account for account in accounts}

    if 'tt_account' not in st.session_state or st.session_state.tt_account not in account_options.values():
        st.session_state.tt_account = next(iter(account_options.values()))

    default_index = list(account_options.values()).index(st.session_state.tt_account)
    selected_option = st.selectbox('Select an account:', list(account_options.keys()), index=default_index)
    st.session_state.tt_account = account_options[selected_option]

    start_date = st.date_input('Start Date', format="YYYY-MM-DD", value=st.session_state.start_date)
    st.session_state.start_date = start_date
    end_date = st.date_input('End Date', format="YYYY-MM-DD", value=st.session_state.end_date)
    st.session_state.end_date = end_date
    
    if (not (username and password)):
        st.subheader('Logout')
        st.button('Logout', on_click=logout)
