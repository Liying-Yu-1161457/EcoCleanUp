from loginapp import app
from loginapp import db
from flask import redirect, render_template, session, url_for, flash, request
from datetime import datetime

def now():
    return datetime.now()

@app.route('/event_leader/home')
def event_leader_home():
     """EventLeader Homepage endpoint.

     Methods:
     - get: Renders the homepage for the current staff user, or an "Access
          Denied" 403: Forbidden page if the current user has a different role.

     If the user is not logged in, requests will redirect to the login page.
     """
     if 'loggedin' not in session:
          return redirect(url_for('login'))
     elif session['role']!='event_leader':
          return render_template('access_denied.html'), 403

     return render_template('event_leader_home.html')

@app.route('/event_leader/create', methods=['GET', 'POST'])
def event_leader_create():
    """create event"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    if request.method == 'POST':
        # get data
        event_name = request.form['event_name']
        location = request.form['location']
        event_type = request.form['event_type']
        event_date = request.form['event_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        duration = request.form.get('duration', 0)
        supplies = request.form.get('supplies', '')
        description = request.form.get('description', '')
        safety_info = request.form.get('safety_info', '')
        
        # verify
        if not event_name or not location or not event_date:
            flash('Please fill in all required fields', 'danger')
            return render_template('event_leader_create.html')
        
        # insert db
        with db.get_cursor() as cursor:
            cursor.execute('''
                INSERT INTO events 
                (event_name, location, event_type, event_date, start_time, end_time, 
                 duration, supplies, description, safety_info, status, event_leader_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'upcoming', %s)
            ''', (event_name, location, event_type, event_date, start_time, end_time,
                  duration, supplies, description, safety_info, session['user_id']))
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('event_leader_my_events'))
    
    return render_template('event_leader_create.html')
