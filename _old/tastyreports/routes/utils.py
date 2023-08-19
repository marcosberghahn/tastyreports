from flask import redirect, request, url_for, session
from tastyreports import app, account_numbers

@app.route('/set_account/<string:account_number>')
def set_account(account_number=None):
    if account_number in account_numbers:
        session['tt_account'] = account_number
    else:
        session['tt_account'] = account_numbers[0]
    return redirect(request.referrer or url_for('home'))
