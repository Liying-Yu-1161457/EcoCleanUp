from flask import redirect, render_template, session, url_for, flash, request
from datetime import datetime

from loginapp import app, db

def now():
    return datetime.now()

@app.route('/event_leader/home')
def event_leader_home():
    """home page for event leaders"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403

    return render_template('event_leader_home.html')

@app.route('/event_leader/create', methods=['GET', 'POST'])
def event_leader_create():
    """create new event"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    if request.method == 'POST':
        # get form data
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
        
        # check required fields
        if not event_name or not location or not event_date:
            flash('Please fill in all required fields', 'danger')
            return render_template('event_leader_create.html')
        
        # save to db
        with db.get_cursor() as cursor:
            cursor.execute('''
                INSERT INTO events 
                (event_name, location, event_type, event_date, start_time, end_time, 
                 duration, supplies, description, safety_info, status, event_leader_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'upcoming', %s)
            ''', (event_name, location, event_type, event_date, start_time, end_time,
                  duration, supplies, description, safety_info, session['user_id']))
        
        flash('Event created!', 'success')
        return redirect(url_for('event_leader_my_events'))
    
    return render_template('event_leader_create.html')

@app.route('/event_leader/my_events')
def event_leader_my_events():
    """show all events created by current user"""
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
    """show single event details"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        # get event
        cursor.execute('''
            SELECT * FROM events 
            WHERE event_id = %s AND event_leader_id = %s
        ''', (event_id, session['user_id']))
        event = cursor.fetchone()
        
        if not event:
            flash('Event not found', 'danger')
            return redirect(url_for('event_leader_my_events'))
        
        # get volunteers
        cursor.execute('''
            SELECT u.user_id, u.username, u.full_name, u.email, u.contact_number,
                   r.registration_time, r.attendance_stat
            FROM registrations r
            JOIN users u ON r.user_id = u.user_id
            WHERE r.event_id = %s
            ORDER BY r.registration_time
        ''', (event_id,))
        registrations = cursor.fetchall()
        
        # get outcomes if any
        cursor.execute('SELECT * FROM outcomes WHERE event_id = %s', (event_id,))
        outcome = cursor.fetchone() or {}
    
        cursor.execute('SELECT COUNT(*) as count FROM feedback WHERE event_id = %s', (event_id,))
        result = cursor.fetchone()
        feedback_count = result['count'] if result else 0

    return render_template('event_leader_event_detail.html', 
                         event=event, 
                         registrations=registrations,
                         outcome=outcome,
                         feedback_count=feedback_count)

@app.route('/event_leader/cancel/<int:event_id>')
def event_leader_cancel_event(event_id):
    """cancel an upcoming event"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        cursor.execute('''
            UPDATE events 
            SET status = 'cancelled' 
            WHERE event_id = %s AND event_leader_id = %s AND status = 'upcoming'
            RETURNING event_id
        ''', (event_id, session['user_id']))
        
        if cursor.fetchone():
            flash('Event cancelled', 'success')
        else:
            flash('Could not cancel event', 'danger')
    
    return redirect(url_for('event_leader_my_events'))

@app.route('/event_leader/record/<int:event_id>', methods=['GET', 'POST'])
def event_leader_record_outcomes(event_id):
    """record event results"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        # check event
        cursor.execute('''
            SELECT * FROM events 
            WHERE event_id = %s AND event_leader_id = %s
        ''', (event_id, session['user_id']))
        event = cursor.fetchone()
        
        if not event:
            flash('Event not found', 'danger')
            return redirect(url_for('event_leader_my_events'))
        
        # check if outcomes exist
        cursor.execute('SELECT * FROM outcomes WHERE event_id = %s', (event_id,))
        outcome = cursor.fetchone()
    
    if request.method == 'POST':
        num_attendees = request.form.get('num_attendees', 0)
        bags_collected = request.form.get('bags_collected', 0)
        recyclables_sorted = request.form.get('recyclables_sorted', 0)
        other_achievements = request.form.get('other_achievements', '')
        
        with db.get_cursor() as cursor:
            if outcome:
                # update
                cursor.execute('''
                    UPDATE outcomes 
                    SET num_attendees = %s, bags_collected = %s, 
                        recyclables_sorted = %s, other_achievements = %s,
                        recorded_at = NOW()
                    WHERE event_id = %s
                ''', (num_attendees, bags_collected, recyclables_sorted, 
                      other_achievements, event_id))
            else:
                # insert
                cursor.execute('''
                    INSERT INTO outcomes 
                    (event_id, num_attendees, bags_collected, recyclables_sorted, 
                     other_achievements, recorded_by, recorded_at)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW())
                ''', (event_id, num_attendees, bags_collected, recyclables_sorted,
                      other_achievements, session['user_id']))
            
            # mark event as completed
            cursor.execute('''
                UPDATE events SET status = 'completed' 
                WHERE event_id = %s
            ''', (event_id,))
        
        flash('Outcomes recorded', 'success')
        return redirect(url_for('event_leader_event_detail', event_id=event_id))
    
    return render_template('event_leader_record_outcomes.html', 
                         event=event, outcome=outcome)

@app.route('/event_leader/attendance/<int:event_id>/<int:user_id>', methods=['POST'])
def event_leader_update_attendance(event_id, user_id):
    """update volunteer attendance status"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    attendance_stat = request.form.get('attendance_stat')
    
    with db.get_cursor() as cursor:
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
            flash('Attendance updated', 'success')
        else:
            flash('Update failed', 'danger')
    
    return redirect(url_for('event_leader_event_detail', event_id=event_id))

@app.route('/event_leader/remove/<int:event_id>/<int:user_id>')
def event_leader_remove_volunteer(event_id, user_id):
    """remove volunteer from event"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        cursor.execute('''
            DELETE FROM registrations r
            USING events e
            WHERE r.event_id = e.event_id 
              AND r.event_id = %s 
              AND r.user_id = %s
              AND e.event_leader_id = %s
        ''', (event_id, user_id, session['user_id']))
        
        if cursor.rowcount > 0:
            flash('Volunteer removed', 'success')
        else:
            flash('Remove failed', 'danger')
    
    return redirect(url_for('event_leader_event_detail', event_id=event_id))

@app.route('/event_leader/feedback/<int:event_id>')
def event_leader_view_feedback(event_id):
    """view feedback for an event"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'event_leader':
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT f.*, u.username, u.full_name
            FROM feedback f
            JOIN users u ON f.user_id = u.user_id
            WHERE f.event_id = %s
            ORDER BY f.submitted_at DESC
        ''', (event_id,))
        feedback = cursor.fetchall()
    
    return render_template('event_leader_feedback.html', feedback=feedback, event_id=event_id)