from flask import Flask, session, redirect, url_for, escape, request
from dotenv import load_dotenv
from tastytrade.session import Session
import os

# Load .env file
load_dotenv()

# Get API credentials from .env file
TT_USERNAME = os.getenv('TT_USERNAME')
TT_PASSWORD = os.getenv('TT_PASSWORD')
TT_ACCOUNT = os.getenv('TT_ACCOUNT')
TT_CERT_ENV = os.getenv('TT_CERT_ENV', False)

app = Flask(__name__)

tt_session = Session(TT_USERNAME, TT_PASSWORD, is_certification=TT_CERT_ENV)

from tastyreports.routes import home
