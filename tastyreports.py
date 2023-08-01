from tastytrade.session import Session
from tastytrade.account import Account
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

if 'account_index' not in st.session_state:
    st.session_state['account_index'] = 0
if 'current_account' not in st.session_state:
    st.session_state['current_account'] = None
if 'sandbox' not in st.session_state:
    st.session_state['sandbox'] = False
if 'tt_session' not in st.session_state:
    st.session_state['tt_session'] = None

st.set_page_config(page_title="tastyreports", page_icon="📈")

def login(username, password, sandbox):
    st.session_state.sandbox = sandbox
    session = Session(username, password, is_certification=sandbox)
    st.session_state.tt_session = session
    account = Account.get_accounts(st.session_state.tt_session)[st.session_state.account_index]
    st.session_state.current_account = account

def logout():
    st.session_state.tt_session = None

if (not st.session_state['tt_session']):
    st.title("Login")

    username = os.getenv('TT_USERNAME', '')
    password = os.getenv('TT_PASSWORD', '')

    username = st.text_input('Username', value=username)
    password = st.text_input('Password', type='password', value=password)
    sandbox = st.checkbox('Certification Environment', value=st.session_state.sandbox)

    st.button('Login', on_click=login, args=[username, password, sandbox])
else:
    st.title("tastyreports")
    st.button('Logout', on_click=logout)
