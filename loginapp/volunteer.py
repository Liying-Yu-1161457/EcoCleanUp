from loginapp import app
from loginapp import db
from flask import redirect, render_template, session, url_for, flash
@app.route('/volunteer/home')
def volunteer_home():
     """Volunteer Homepage endpoint.

     Methods:
     - get: Renders the homepage for the current customer, or an "Access
          Denied" 403: Forbidden page if the current user has a different role.

     If the user is not logged in, requests will redirect to the login page.
     """
     # Note: You'll need to use "logged in" and role checks like the ones below
     # on every single endpoint that should be restricted to logged-in users,
     # or users with a certain role. Otherwise, anyone who knows the URL can
     # access that page.
     #
     # In this example we've just repeated the code everywhere (you'll see the
     # same checks in staff.py and admin.py), but it would be a great idea to
     # extract these checks into reusable functions. You could place them in
     # user.py with the rest of the login system, for example, and import them
     # into other modules as necessary.
     #
     # One common way to implement login and role checks in Flask is with "View
     # Decorators", such as the "login_required" example in the official
     # tutorial [1]. If you choose to use that approach, you'll need to adapt
     # it a little to our project, as we don't store the username in `g.user`.
     #
     # References:
     # [1] https://flask.palletsprojects.com/en/stable/patterns/viewdecorators/

     if 'loggedin' not in session:
          # The user isn't logged in, so redirect them to the login page.
          return redirect(url_for('login'))
     elif session['role']!='volunteer':
          # The user isn't logged in with a customer account, so return an
          # "Access Denied" page instead. We don't do a redirect here, because
          # we're not sending them somewhere else: just delivering an
          # alternative page.
          # 
          # Note: the '403' below returns HTTP status code 403: Forbidden to the
          # browser, indicating that the user was not allowed to access the
          # requested page.
          return render_template('access_denied.html'), 403

     # The user is logged in with a customer account, so render the customer
     # homepage as requested.
     return render_template('volunteer_home.html')

@app.route('/volunteer/events')
def volunteer_events():
    """display all events"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'volunteer':
        return render_template('access_denied.html'), 403
    
    # get all events from database
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT event_id, event_name, location, event_date, start_time, end_time, 
                   description, supplies, safety_info, event_type
            FROM events 
            WHERE status = 'upcoming' 
            ORDER BY event_date, start_time
        ''')
        events = cursor.fetchall()
    
    return render_template('volunteer_events.html', events=events)
@app.route('/volunteer/event/<int:event_id>')
def volunteer_event_detail(event_id):
    """display each event detail"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'volunteer':
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        # get detail from database
        cursor.execute('''
            SELECT e.*, u.full_name as leader_name
            FROM events e
            LEFT JOIN users u ON e.event_leader_id = u.user_id
            WHERE e.event_id = %s
        ''', (event_id,))
        event = cursor.fetchone()
        
        if not event:
            return render_template('404.html'), 404
        
        # check current user has attent or not.
        cursor.execute('''
            SELECT registration_id, attendance_stat 
            FROM registrations 
            WHERE user_id = %s AND event_id = %s
        ''', (session['user_id'], event_id))
        registration = cursor.fetchone()
        
    return render_template('volunteer_event_detail.html', 
                         event=event, 
                         registered=registration is not None,
                         registration=registration)

@app.route('/volunteer/register/<int:event_id>', methods=['POST'])
def volunteer_register(event_id):
    """volunteer register"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'volunteer':
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        # 1. check event is exist
        cursor.execute('''
            SELECT event_date, start_time, end_time, status 
            FROM events 
            WHERE event_id = %s
        ''', (event_id,))
        event = cursor.fetchone()
        
        if not event:
            return "Event not found", 404
        
        if event['status'] != 'upcoming':
            return "This event is no longer available for registration", 400
        
        # 2. check registered or not 
        cursor.execute('''
            SELECT registration_id FROM registrations 
            WHERE user_id = %s AND event_id = %s
        ''', (session['user_id'], event_id))
        
        if cursor.fetchone():
            flash('You are already registered for this event.', 'warning')
            return redirect(url_for('volunteer_event_detail', event_id=event_id))
        
        # 3. check duty conflict
        cursor.execute('''
            SELECT e.event_id, e.event_name, e.event_date, e.start_time, e.end_time
            FROM registrations r
            JOIN events e ON r.event_id = e.event_id
            WHERE r.user_id = %s 
              AND e.event_date = %s
              AND r.attendance_stat IN ('registered', 'attended')
              AND NOT (e.end_time <= %s OR e.start_time >= %s)
        ''', (session['user_id'], event['event_date'], 
              event['start_time'], event['end_time']))
        
        conflicting_event = cursor.fetchone()
        
        if conflicting_event:
            flash(
                f'Cannot register: You already have an event "{conflicting_event["event_name"]}" '
                f'on {conflicting_event["event_date"]} '
                f'from {conflicting_event["start_time"]} to {conflicting_event["end_time"]}.',
                'danger'
            )
            return redirect(url_for('volunteer_event_detail', event_id=event_id))
        
        # 4. commit register
        cursor.execute('''
            INSERT INTO registrations (user_id, event_id, registration_time, attendance_stat)
            VALUES (%s, %s, NOW(), 'registered')
        ''', (session['user_id'], event_id))
        
        flash('Successfully registered for the event!', 'success')
    
    return redirect(url_for('volunteer_event_detail', event_id=event_id))

@app.route('/volunteer/history')
def volunteer_history():
    """display history"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'volunteer':
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        # get all members 
        cursor.execute('''
            SELECT 
                e.event_id,
                e.event_name,
                e.location,
                e.event_date,
                e.start_time,
                e.end_time,
                r.registration_time,
                r.attendance_stat,
                CASE 
                    WHEN e.event_date < CURRENT_DATE THEN 'past'
                    WHEN e.event_date = CURRENT_DATE AND e.end_time <= CURRENT_TIME THEN 'past'
                    ELSE 'upcoming'
                END as event_status,
                f.rating,
                f.comments as feedback_comment,
                f.submitted_at
            FROM registrations r
            JOIN events e ON r.event_id = e.event_id
            LEFT JOIN feedback f ON r.user_id = f.user_id AND r.event_id = f.event_id
            WHERE r.user_id = %s
            ORDER BY e.event_date DESC, e.start_time DESC
        ''', (session['user_id'],))
        history = cursor.fetchall()
    
    return render_template('volunteer_history.html', history=history)