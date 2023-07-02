from datetime import datetime, timedelta
from flask import render_template, redirect, request, url_for, session
from tastyreports import app, tt_session, account_numbers
from tastytrade.account import Account, AccountBalance, AccountBalanceSnapshot

@app.route('/pl_calendar', methods=['GET', 'POST'])
def pl_calendar(account_number=None, start_date=None, end_date=None):
    if account_number is None:
        account_number = session.get('current_account')

    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        session['start_date'] = start_date
        session['end_date'] = end_date

    if 'start_date' in session and session['start_date'] is not None:
        start_date = session['start_date']
    else:
        start_date = datetime.today().replace(day=1).strftime('%Y-%m-%d')

    if 'end_date' in session and session['end_date'] is not None:
        end_date = session['end_date']
    else:
        end_date = datetime.today().strftime('%Y-%m-%d')
    
    account = Account.get_account(tt_session, account_number)
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    snapshots = []

    delta = end_date_obj - start_date_obj
    for i in range(delta.days + 1):
        day = start_date_obj + timedelta(days=i)
        day_snapshot = account.get_balance_snapshots(tt_session, day.date(), 'EOD')
        snapshots.extend(day_snapshot)
    
    snapshots = [snapshot for snapshot in snapshots if snapshot.time_of_day is not None]
    snapshots.sort(key=lambda snapshot: snapshot.snapshot_date)

    return render_template('pl_calendar.html', account_numbers=account_numbers, current_account=account_number, start_date=start_date, end_date=end_date, data=snapshots)
