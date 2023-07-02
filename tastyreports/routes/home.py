from datetime import datetime
from flask import render_template, redirect, request, url_for, session
from tastyreports import app, tt_session, account_numbers
from tastytrade.account import Account, AccountBalance, AccountBalanceSnapshot

@app.route('/')
@app.route('/home')
def home():
    account_number = session.get('current_account')
    if account_number is None or account_number not in account_numbers:
        account_number = account_numbers[0]

    if account_number is None:
        return 'No accounts available', 404

    account = Account.get_account(tt_session, account_number)
    balances = account.get_balances(tt_session)
    return render_template('home.html', account_numbers=account_numbers, current_account=account_number, account=account, balances=balances)
