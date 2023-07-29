from tastytrade.session import Session
from tastytrade.account import Account
import streamlit as st
import pandas as pd
import numpy as np

if 'account_index' not in st.session_state:
    st.session_state['account_index'] = 0
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = 0
if 'sandbox' not in st.session_state:
    st.session_state['sandbox'] = True
if 'tt_session' not in st.session_state:
    st.session_state['tt_session'] = None

st.set_page_config(
    page_title="tastyreports", 
    page_icon="assets/icon-cropped.png"
)

def nav_to(url):
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (url)
    st.write(nav_script, unsafe_allow_html=True)

def login(username, password, sandbox):
    if (not username) or (not password):
        st.session_state.logged_in = 0
        st.session_state.tt_session = None
        return
    st.session_state.sandbox = sandbox
    st.session_state.tt_session = Session(username, password, is_certification=sandbox)
    st.session_state.logged_in = 1

if (not st.session_state['logged_in']):
    st.title("Login")
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    sandbox = st.checkbox('Certification Environment', value=st.session_state.sandbox)

    st.button('Login', on_click=login, args=[username, password, sandbox])
else:
    st.title("tastyreports")
    st.button('Logout', on_click=login, args=[None, None, True])
