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

from tastyreports.routes import home, utils, pl_calendar, pl_chart
