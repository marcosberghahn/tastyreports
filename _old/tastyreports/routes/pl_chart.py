from datetime import datetime
from flask import render_template, redirect, request, url_for, session
from tastyreports import app, tt_session, account_numbers
from tastytrade.account import Account, AccountBalance, AccountBalanceSnapshot

@app.route('/pl_chart')
def pl_chart(account_number=None, start_date=None, end_date=None):
    if account_number is None:
        account_number = session.get('current_account')

    if start_date is None:
        start_date = datetime.today().replace(day=1)

    if end_date is None:
        end_date = datetime.today()

    return render_template('pl_chart.html', account_numbers=account_numbers, current_account=account_number, start_date=start_date, end_date=end_date)
