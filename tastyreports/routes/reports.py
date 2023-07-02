from datetime import datetime
from flask import render_template, redirect, request, url_for, session
from tastyreports import app, tt_session
from tastytrade.account import Account

def get_account_numbers():
    accounts = Account.get_accounts(tt_session)
    return [account.account_number for account in accounts]

account_numbers = get_account_numbers()

@app.route('/')
@app.route('/account/')
def index():
    # Handle empty list of account numbers
    default_account_number = account_numbers[0] if account_numbers else None

    if default_account_number is None:
        return 'No accounts available', 404
    else:
        session['current_account'] = default_account_number
        return redirect(url_for('home'))

@app.route('/home')
def home():
    account_number = session.get('current_account')
    # Check if 'current_account' is in session
    if account_number is None:
        print("Error: 'current_account' not found in session.")
        # Handle the error, e.g., redirect to login page or show an error message
    else:
        # Handles when account_number is None or not in account_numbers list
        if not account_number or account_number not in account_numbers:
            account_number = account_numbers[0] if account_numbers else None
            session['current_account'] = account_number

        if account_number is None:
            return 'No accounts available', 404

        return render_template('home.html', account_numbers=account_numbers, current_account=account_number)

@app.route('/set_account/<string:account_number>')
def set_account(account_number=None):
    if account_number in account_numbers:
        session['current_account'] = account_number
    else:
        session['current_account'] = account_numbers[0]
    return redirect(request.referrer or url_for('home'))

@app.route('/pl_calendar')
def pl_calendar(account_number=None, start_date=None, end_date=None):
    if account_number is None:
        account_number = session.get('current_account')

    if start_date is None:
        start_date = datetime.today().replace(day=1)

    if end_date is None:
        end_date = datetime.today()

    return render_template('pl_calendar.html', account_numbers=account_numbers, current_account=account_number, start_date=start_date, end_date=end_date)
