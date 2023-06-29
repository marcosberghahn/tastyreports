from flask import render_template
from tastyreports import app, tt_session

@app.route('/')
def home():
    foo = 'bar'

    return render_template('home.html', data=foo)
