from tastytrade.session import Session
from tastytrade.account import Account
import streamlit as st

st.set_page_config(page_title="Account", page_icon="📈")

def login(username, password, sandbox):
    st.session_state.sandbox = sandbox
    st.session_state.tt_session = Session(username, password, is_certification=sandbox)
    st.session_state.logged_in = 1

def nav_to(url):
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (url)
    st.write(nav_script, unsafe_allow_html=True)

if (st.session_state['logged_in']):
    st.title("Account")
    accounts = Account.get_accounts(st.session_state.tt_session)
    account = Account.get_accounts(st.session_state.tt_session)[st.session_state.account_index]
    st.write(accounts)
    st.button('Logout', on_click=login, args=[None, None, None])
else:
    nav_to('/')
