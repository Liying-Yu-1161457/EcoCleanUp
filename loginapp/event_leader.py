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

@app.route('/event_leader/my_events')
def event_leader_my_events():
    """list all current user's events"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT event_id, event_name, location, event_date, start_time, end_time,
                   status, 
                   (SELECT COUNT(*) FROM registrations WHERE event_id = events.event_id) as volunteer_count
            FROM events 
            WHERE event_leader_id = %s
            ORDER BY 
                CASE WHEN status = 'upcoming' THEN 1 ELSE 2 END,
                event_date ASC
        ''', (session['user_id'],))
        events = cursor.fetchall()
    
    return render_template('event_leader_my_events.html', events=events)

@app.route('/event_leader/event/<int:event_id>')
def event_leader_event_detail(event_id):
    """view event detail """
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        # get event detail
        cursor.execute('''
            SELECT * FROM events 
            WHERE event_id = %s AND event_leader_id = %s
        ''', (event_id, session['user_id']))
        event = cursor.fetchone()
        
        if not event:
            flash('Event not found or you do not have permission to view it.', 'danger')
            return redirect(url_for('event_leader_my_events'))
        
        # list volunteer of event
        cursor.execute('''
            SELECT u.user_id, u.username, u.full_name, u.email, u.contact_number,
                   r.registration_time, r.attendance_stat
            FROM registrations r
            JOIN users u ON r.user_id = u.user_id
            WHERE r.event_id = %s
            ORDER BY r.registration_time
        ''', (event_id,))
        registrations = cursor.fetchall()
        
        # get outcomes
        cursor.execute('SELECT * FROM outcomes WHERE event_id = %s', (event_id,))
        outcome = cursor.fetchone() or {}
    
    return render_template('event_leader_event_detail.html', 
                         event=event, 
                         registrations=registrations,
                         outcome=outcome)

@app.route('/event_leader/cancel/<int:event_id>')
def event_leader_cancel_event(event_id):
    """cancel event"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        # check event owner
        cursor.execute('''
            UPDATE events 
            SET status = 'cancelled' 
            WHERE event_id = %s AND event_leader_id = %s AND status = 'upcoming'
            RETURNING event_id
        ''', (event_id, session['user_id']))
        
        if cursor.fetchone():
            flash('Event cancelled successfully.', 'success')
        else:
            flash('Event not found, already cancelled, or you do not have permission.', 'danger')
    
    return redirect(url_for('event_leader_my_events'))

@app.route('/event_leader/record/<int:event_id>', methods=['GET', 'POST'])
def event_leader_record_outcomes(event_id):
    """register outcomes"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        # check event is current user join
        cursor.execute('''
            SELECT * FROM events 
            WHERE event_id = %s AND event_leader_id = %s
        ''', (event_id, session['user_id']))
        event = cursor.fetchone()
        
        if not event:
            flash('Event not found or you do not have permission.', 'danger')
            return redirect(url_for('event_leader_my_events'))
        
        # check outcome is exist
        cursor.execute('SELECT * FROM outcomes WHERE event_id = %s', (event_id,))
        outcome = cursor.fetchone()
    
    if request.method == 'POST':
        num_attendees = request.form.get('num_attendees', 0)
        bags_collected = request.form.get('bags_collected', 0)
        recyclables_sorted = request.form.get('recyclables_sorted', 0)
        other_achievements = request.form.get('other_achievements', '')
        
        with db.get_cursor() as cursor:
            if outcome:
                # update record
                cursor.execute('''
                    UPDATE outcomes 
                    SET num_attendees = %s, bags_collected = %s, 
                        recyclables_sorted = %s, other_achievements = %s,
                        recorded_at = NOW()
                    WHERE event_id = %s
                ''', (num_attendees, bags_collected, recyclables_sorted, 
                      other_achievements, event_id))
            else:
                # create record
                cursor.execute('''
                    INSERT INTO outcomes 
                    (event_id, num_attendees, bags_collected, recyclables_sorted, 
                     other_achievements, recorded_by, recorded_at)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW())
                ''', (event_id, num_attendees, bags_collected, recyclables_sorted,
                      other_achievements, session['user_id']))
            
            # update completed
            cursor.execute('''
                UPDATE events SET status = 'completed' 
                WHERE event_id = %s
            ''', (event_id,))
        
        flash('Event outcomes recorded successfully!', 'success')
        return redirect(url_for('event_leader_event_detail', event_id=event_id))
    
    return render_template('event_leader_record_outcomes.html', 
                         event=event, outcome=outcome)

@app.route('/event_leader/attendance/<int:event_id>/<int:user_id>', methods=['POST'])
def event_leader_update_attendance(event_id, user_id):
    """upate volunteer attendance stat"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    attendance_stat = request.form.get('attendance_stat')
    
    with db.get_cursor() as cursor:
        # confirm current event leader
        cursor.execute('''
            UPDATE registrations r
            SET attendance_stat = %s
            FROM events e
            WHERE r.event_id = e.event_id 
              AND r.event_id = %s 
              AND r.user_id = %s
              AND e.event_leader_id = %s
        ''', (attendance_stat, event_id, user_id, session['user_id']))
        
        if cursor.rowcount > 0:
            flash('Attendance updated successfully.', 'success')
        else:
            flash('Failed to update attendance.', 'danger')
    
    return redirect(url_for('event_leader_event_detail', event_id=event_id))

@app.route('/event_leader/remove/<int:event_id>/<int:user_id>')
def event_leader_remove_volunteer(event_id, user_id):
    """remove event_leader"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        # confirm event leader
        cursor.execute('''
            DELETE FROM registrations r
            USING events e
            WHERE r.event_id = e.event_id 
              AND r.event_id = %s 
              AND r.user_id = %s
              AND e.event_leader_id = %s
        ''', (event_id, user_id, session['user_id']))
        
        if cursor.rowcount > 0:
            flash('Volunteer removed from event.', 'success')
        else:
            flash('Failed to remove volunteer.', 'danger')
    
    return redirect(url_for('event_leader_event_detail', event_id=event_id))