from flask import redirect, render_template, session, url_for, flash, request
from loginapp import app, db

@app.route('/admin/users')
def admin_users():
    """view all users"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403
    
    # get query parameters
    search = request.args.get('search', '')
    role_filter = request.args.get('role', '')
    status_filter = request.args.get('status', '')
    
    with db.get_cursor() as cursor:
        # process query sql
        query = '''
            SELECT user_id, username, email, full_name, role, status, 
                   created_at,profile_image,
                   (SELECT COUNT(*) FROM events WHERE event_leader_id = users.user_id) as event_count,
                   (SELECT COUNT(*) FROM registrations WHERE user_id = users.user_id) as registration_count
            FROM users
            WHERE 1=1
        '''
        params = []
        
        if search:
            query += ' AND (username ILIKE %s OR full_name ILIKE %s OR email ILIKE %s)'
            search_param = f'%{search}%'
            params.extend([search_param, search_param, search_param])
        
        if role_filter:
            query += ' AND role = %s'
            params.append(role_filter)
        
        if status_filter:
            query += ' AND status = %s'
            params.append(status_filter)
        
        query += ' ORDER BY user_id'
        
        cursor.execute(query, params)
        users = cursor.fetchall()
    
    return render_template('admin_users.html', 
                         users=users, 
                         search=search,
                         role_filter=role_filter,
                         status_filter=status_filter)

@app.route('/admin/user/<int:user_id>/toggle')
def admin_toggle_status(user_id):
    """switch user status"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403
    
    # cannot make owner status
    if user_id == session['user_id']:
        flash('You cannot change your own status.', 'warning')
        return redirect(url_for('admin_users'))
    
    with db.get_cursor() as cursor:
        cursor.execute('''
            UPDATE users 
            SET status = CASE WHEN status = 'active'::user_status THEN 'inactive'::user_status
                ELSE 'active'::user_status END
            WHERE user_id = %s AND role != 'admin'
            RETURNING username, status
        ''', (user_id,))
        
        result = cursor.fetchone()
        if result:
            flash(f'User {result["username"]} is now {result["status"]}.', 'success')
        else:
            flash('User not found or cannot be modified.', 'danger')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/user/<int:user_id>')
def admin_user_detail(user_id):
    """view user detail"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT user_id, username, email, full_name, contact_number, home_address, 
                   environmental_interests, role, status, created_at,
                   profile_image
            FROM users 
            WHERE user_id = %s
        ''', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('admin_users'))
        
        # get user's event
        if user['role'] == 'event_leader':
            cursor.execute('''
                SELECT event_id, event_name, event_date, status,
                       (SELECT COUNT(*) FROM registrations WHERE event_id = events.event_id) as volunteers
                FROM events
                WHERE event_leader_id = %s
                ORDER BY event_date DESC
            ''', (user_id,))
            user['events'] = cursor.fetchall()
        
        # get user apply event
        if user['role'] == 'volunteer':
            cursor.execute('''
                SELECT e.event_id, e.event_name, e.event_date, e.location,
                       r.registration_time, r.attendance_stat
                FROM registrations r
                JOIN events e ON r.event_id = e.event_id
                WHERE r.user_id = %s
                ORDER BY e.event_date DESC
            ''', (user_id,))
            user['registrations'] = cursor.fetchall()
    
    return render_template('admin_user_detail.html', user=user)

@app.route('/admin/home')
def admin_home():
    """Admin Homepage"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403
    
    return render_template('admin_home.html')

@app.route('/admin/reports')
def admin_reports():
    """generate reports"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        # 1. calculate reports
        cursor.execute('''
            SELECT 
                (SELECT COUNT(*) FROM users WHERE role = 'volunteer') as total_volunteers,
                (SELECT COUNT(*) FROM users WHERE role = 'event_leader') as total_leaders,
                (SELECT COUNT(*) FROM users WHERE role = 'admin') as total_admins,
                (SELECT COUNT(*) FROM events) as total_events,
                (SELECT COUNT(*) FROM events WHERE status = 'upcoming') as upcoming_events,
                (SELECT COUNT(*) FROM events WHERE status = 'completed') as completed_events,
                (SELECT COUNT(*) FROM registrations) as total_registrations,
                (SELECT COUNT(*) FROM feedback) as total_feedback,
                (SELECT COALESCE(AVG(rating), 0) FROM feedback) as avg_rating
        ''')
        stats = cursor.fetchone()
        
        # 2. monthy event reports
        cursor.execute('''
            SELECT 
                TO_CHAR(event_date, 'YYYY-MM') as month,
                COUNT(*) as event_count,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_count
            FROM events
            GROUP BY TO_CHAR(event_date, 'YYYY-MM')
            ORDER BY month DESC
            LIMIT 6
        ''')
        monthly_events = cursor.fetchall()
        
        # 3. top volunteer events
        cursor.execute('''
            SELECT 
                e.event_id,
                e.event_name,
                e.event_date,
                COUNT(r.registration_id) as registration_count,
                COUNT(DISTINCT CASE WHEN r.attendance_stat = 'attended' THEN r.user_id END) as attended_count
            FROM events e
            LEFT JOIN registrations r ON e.event_id = r.event_id
            GROUP BY e.event_id, e.event_name, e.event_date
            ORDER BY registration_count DESC
            LIMIT 5
        ''')
        top_events = cursor.fetchall()
        
        # 4. most active volunteer
        cursor.execute('''
            SELECT 
                u.user_id,
                u.username,
                u.full_name,
                COUNT(r.registration_id) as registrations,
                COUNT(CASE WHEN r.attendance_stat = 'attended' THEN 1 END) as attended_events,
                COUNT(f.feedback_id) as feedback_count
            FROM users u
            LEFT JOIN registrations r ON u.user_id = r.user_id
            LEFT JOIN feedback f ON u.user_id = f.user_id
            WHERE u.role = 'volunteer'
            GROUP BY u.user_id, u.username, u.full_name
            HAVING COUNT(r.registration_id) > 0
            ORDER BY attended_events DESC
            LIMIT 5
        ''')
        top_volunteers = cursor.fetchall()
        
        # 5. events location distribute
        cursor.execute('''
            SELECT 
                event_type,
                COUNT(*) as count
            FROM events
            GROUP BY event_type
            ORDER BY count DESC
        ''')
        event_types = cursor.fetchall()
    
    return render_template('admin_reports.html',
                         stats=stats,
                         monthly_events=monthly_events,
                         top_events=top_events,
                         top_volunteers=top_volunteers,
                         event_types=event_types)

@app.route('/admin/user/<int:user_id>/role', methods=['POST'])
def admin_change_role(user_id):
    """change user role"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    elif session['role'] != 'admin':
        return render_template('access_denied.html'), 403
    
    new_role = request.form.get('role')
    
    with db.get_cursor() as cursor:
        cursor.execute('''
            UPDATE users 
            SET role = %s 
            WHERE user_id = %s AND role != 'admin'
        ''', (new_role, user_id))
        
        if cursor.rowcount > 0:
            flash('User role updated', 'success')
        else:
            flash('Cannot change admin role', 'danger')
    
    return redirect(url_for('admin_users'))