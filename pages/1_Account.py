from tastytrade import Account
import streamlit as st

st.set_page_config(page_title="Account", page_icon="📈")

st.title("Account")

accounts = Account.get_accounts(st.session_state.tt_session)
account_options = {f"{account.account_number} - {account.nickname}": account for account in accounts}

if 'tt_account' not in st.session_state or st.session_state.tt_account not in account_options.values():
    st.session_state.tt_account = next(iter(account_options.values()))

default_index = list(account_options.values()).index(st.session_state.tt_account)
selected_option = st.selectbox('Select an account:', list(account_options.keys()), index=default_index)
st.session_state.tt_account = account_options[selected_option]

st.write(st.session_state.tt_account)
