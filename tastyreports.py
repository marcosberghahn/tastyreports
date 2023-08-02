from tastytrade.session import Session
from tastytrade.account import Account
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

if 'current_account' not in st.session_state:
    st.session_state['current_account'] = None
if 'sandbox' not in st.session_state:
    st.session_state['sandbox'] = os.getenv('SANDBOX', False)
if 'tt_session' not in st.session_state:
    st.session_state['tt_session'] = None
if 'start_date' not in st.session_state:
    st.session_state['start_date'] = None
if 'end_date' not in st.session_state:
    st.session_state['end_date'] = None

st.set_page_config(page_title="tastyreports", page_icon="📈")

def login(username, password, sandbox):
    st.session_state.sandbox = sandbox
    session = Session(username, password, is_certification=sandbox)
    st.session_state.tt_session = session
    account = Account.get_accounts(st.session_state.tt_session)[0]
    st.session_state.current_account = account

def logout():
    st.session_state.tt_session = None

username = os.getenv('TT_USERNAME', '')
password = os.getenv('TT_PASSWORD', '')

if (username and password and not st.session_state['tt_session']):
    login(username, password, st.session_state.sandbox)

if (not st.session_state['tt_session']):
    st.title("Login")
    form_username = st.text_input('Username', value=username)
    form_password = st.text_input('Password', type='password', value=password)
    sandbox = st.checkbox('Certification Environment', value=st.session_state.sandbox)

    st.button('Login', on_click=login, args=[form_username, form_password, sandbox])
else:
    st.title("tastyreports")
    st.subheader('Settings')

    accounts = Account.get_accounts(st.session_state.tt_session)
    account_options = {f"{account.account_number} - {account.nickname}": account for account in accounts}

    if 'current_account' not in st.session_state or st.session_state.current_account not in account_options.values():
        st.session_state.current_account = next(iter(account_options.values()))

    default_index = list(account_options.values()).index(st.session_state.current_account)
    selected_option = st.selectbox('Select an account:', list(account_options.keys()), index=default_index)
    st.session_state.current_account = account_options[selected_option]

    start_date = st.date_input('Start Date', format="YYYY-MM-DD", value=st.session_state.start_date)
    st.session_state.start_date = start_date
    end_date = st.date_input('End Date', format="YYYY-MM-DD", value=st.session_state.end_date)
    st.session_state.end_date = end_date
    
    if (not username and password):
        st.subheader('Logout')
        st.button('Logout', on_click=logout)
