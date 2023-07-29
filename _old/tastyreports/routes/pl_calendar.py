from datetime import datetime, timedelta
from flask import render_template, redirect, request, url_for, session
from tastyreports import app, tt_session, account_numbers
from tastytrade.account import Account, AccountBalance, AccountBalanceSnapshot
import json

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

    # Fetch snapshot of the day before start_date
    prev_day = start_date_obj
    prev_snapshot = None
    while not prev_snapshot:
        prev_day -= timedelta(days=1)
        snapshots_prev_day = account.get_balance_snapshots(tt_session, prev_day.date(), 'EOD')
        if snapshots_prev_day:
            prev_snapshot = snapshots_prev_day[0]

    delta = end_date_obj - start_date_obj
    for i in range(delta.days + 1):
        day = start_date_obj + timedelta(days=i)
        day_snapshot = account.get_balance_snapshots(tt_session, day.date(), 'EOD')
        snapshots.extend(day_snapshot)

    snapshots = [snapshot for snapshot in snapshots if snapshot.time_of_day is not None]
    snapshots.sort(key=lambda snapshot: snapshot.snapshot_date)

    calendar = []
    prev_net_liquidating_value = prev_snapshot.net_liquidating_value if prev_snapshot else None

    for snapshot in snapshots:
        # Calculate percentage change from the previous day
        if prev_net_liquidating_value is not None:
            net_liquidating_value_pct_change = ((snapshot.net_liquidating_value - prev_net_liquidating_value) / prev_net_liquidating_value) * 100
            net_liquidating_value_change = (snapshot.net_liquidating_value - prev_net_liquidating_value)
            buying_power_used = prev_snapshot.net_liquidating_value - prev_snapshot.derivative_buying_power - prev_snapshot.pending_cash
            return_on_capital = (net_liquidating_value_change / buying_power_used) * 100 if buying_power_used != 0 else 0
            buying_power_pct_used = (buying_power_used / snapshot.net_liquidating_value) * 100 if snapshot.net_liquidating_value != 0 else 0  # Calculate percentage of buying power used
        else:
            net_liquidating_value_pct_change = 0
            net_liquidating_value_change = 0
            buying_power_used = 0
            return_on_capital = 0
            buying_power_pct_used = 0

        # Add snapshot data to list
        calendar.append({
            'date': snapshot.snapshot_date.strftime('%Y-%m-%d'),
            'net_liquidating_value': float(snapshot.net_liquidating_value),
            'net_liquidating_value_change': float(net_liquidating_value_change),
            'net_liquidating_value_pct_change': float(net_liquidating_value_pct_change),
            'buying_power_used': float(buying_power_used),
            'return_on_capital': float(return_on_capital),
            'buying_power_pct_used': float(buying_power_pct_used)
        })

        prev_net_liquidating_value = snapshot.net_liquidating_value
        prev_snapshot = snapshot

    calendar_json = json.dumps(calendar)

    return render_template('pl_calendar.html', account_numbers=account_numbers, current_account=account_number, start_date=start_date, end_date=end_date, data=calendar_json, snapshots=snapshots)
