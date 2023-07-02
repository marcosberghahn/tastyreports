from flask import Flask, session, redirect, url_for, escape, request
from dotenv import load_dotenv
from tastytrade.session import Session
from tastytrade.account import Account
import os

# Load .env file
load_dotenv()

# Get API credentials from .env file
TT_USERNAME = os.getenv('TT_USERNAME')
TT_PASSWORD = os.getenv('TT_PASSWORD')
TT_CERT_ENV = os.getenv('TT_CERT_ENV', False)

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'changeit')

tt_session = Session(TT_USERNAME, TT_PASSWORD, is_certification=TT_CERT_ENV)

def get_account_numbers():
    accounts = Account.get_accounts(tt_session)
    return [account.account_number for account in accounts]

account_numbers = get_account_numbers()

@app.route('/set_account/<string:account_number>')
def set_account(account_number=None):
    if account_number in account_numbers:
        session['current_account'] = account_number
    else:
        session['current_account'] = account_numbers[0]
    return redirect(request.referrer or url_for('home'))

from tastyreports.routes import reports
