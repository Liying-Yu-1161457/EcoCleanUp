from flask import redirect, render_template, request, session, url_for, flash
from flask_bcrypt import Bcrypt
import re

from loginapp import app, db

flask_bcrypt = Bcrypt(app)
DEFAULT_USER_ROLE = 'volunteer'

def user_home_url():
    """get home page url based on role"""
    if 'loggedin' in session:
        role = session.get('role', None)

        if role == 'volunteer':
            return url_for('volunteer_home')
        elif role == 'event_leader':
            return url_for('event_leader_home')
        elif role == 'admin':
            return url_for('admin_home')
        else:
            return url_for('logout')
    return url_for('login')

@app.route('/')
def root():
    """redirect to home or login"""
    return redirect(user_home_url())

@app.route('/login', methods=['GET', 'POST'])

def login():
    """login page - same form for all"""
    if 'loggedin' in session:
        return redirect(user_home_url())

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with db.get_cursor() as cursor:
            cursor.execute('''
                SELECT user_id, username, password_hash, role
                FROM users
                WHERE username = %s
            ''', (username,))
            user = cursor.fetchone()

            if user:
                if flask_bcrypt.check_password_hash(user['password_hash'], password):
                    session['loggedin'] = True
                    session['user_id'] = user['user_id']
                    session['username'] = user['username']
                    session['role'] = user['role']
                    
                    if user['role'] == 'volunteer':
                        with db.get_cursor() as cursor2:
                            cursor2.execute('''
                                SELECT COUNT(*) as count, 
                                       array_agg(e.event_name) as event_names
                                FROM registrations r
                                JOIN events e ON r.event_id = e.event_id
                                WHERE r.user_id = %s 
                                  AND e.event_date >= CURRENT_DATE
                                  AND r.attendance_stat = 'registered'
                            ''', (user['user_id'],))
                            reminder = cursor2.fetchone()
                            
                            if reminder and reminder['count'] > 0:
                                if reminder['count'] == 1:
                                    flash(f'Reminder: You have 1 upcoming event: {reminder["event_names"][0]}', 'info')
                                else:
                                    events_list = ', '.join(reminder['event_names'][:3])
                                    if reminder['count'] > 3:
                                        flash(f'Reminder: You have {reminder["count"]} upcoming events including {events_list}...', 'info')
                                    else:
                                        flash(f'Reminder: You have {reminder["count"]} upcoming events: {events_list}', 'info')
                    
                    return redirect(user_home_url())
                else:
                    return render_template('login.html', username=username, password_invalid=True)
            else:
                return render_template('login.html', username=username, username_invalid=True)

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """register new volunteer"""
    if 'loggedin' in session:
        return redirect(user_home_url())

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form.get('full_name', '')
        phone = request.form.get('phone', '')
        address = request.form.get('address', '')
        interests = request.form.get('interests', '')

        username_error = None
        email_error = None
        password_error = None

        # check username
        with db.get_cursor() as cursor:
            cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
            if cursor.fetchone():
                username_error = 'Username already taken'

        if not re.match(r'^[A-Za-z0-9]+$', username):
            username_error = 'Letters and numbers only'

        # check email
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            email_error = 'Invalid email'

        # check password
        if len(password) < 8:
            password_error = 'Password too short (min 8 chars)'

        if username_error or email_error or password_error:
            return render_template('signup.html',
                                 username=username,
                                 email=email,
                                 full_name=full_name,
                                 phone=phone,
                                 address=address,
                                 interests=interests,
                                 username_error=username_error,
                                 email_error=email_error,
                                 password_error=password_error)

        # create account
        password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

        with db.get_cursor() as cursor:
            cursor.execute('''
                INSERT INTO users 
                (username, password_hash, email, role, full_name, contact_number, home_address, environmental_interests)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (username, password_hash, email, DEFAULT_USER_ROLE, full_name, phone, address, interests))

        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/profile')
def profile():
    """show user profile"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT username, email, full_name, contact_number, home_address, environmental_interests, role
            FROM users WHERE user_id = %s
        ''', (session['user_id'],))
        profile = cursor.fetchone()

    return render_template('profile.html', profile=profile)

@app.route('/profile/edit', methods=['GET', 'POST'])
def profile_edit():
    """edit user info"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        full_name = request.form['full_name']
        phone = request.form['phone']
        address = request.form['address']
        interests = request.form['interests']

        with db.get_cursor() as cursor:
            cursor.execute('''
                UPDATE users 
                SET full_name = %s, contact_number = %s, home_address = %s, environmental_interests = %s
                WHERE user_id = %s
            ''', (full_name, phone, address, interests, session['user_id']))

        flash('Profile updated', 'success')
        return redirect(url_for('profile'))

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT username, email, full_name, contact_number, home_address, environmental_interests, role
            FROM users WHERE user_id = %s
        ''', (session['user_id'],))
        user = cursor.fetchone()

    return render_template('profile_edit.html', user=user)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """change password"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        current = request.form['current_password']
        new = request.form['new_password']
        confirm = request.form['confirm_password']

        if new != confirm:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('change_password'))

        if len(new) < 8:
            flash('Password too short (min 8 chars)', 'danger')
            return redirect(url_for('change_password'))

        with db.get_cursor() as cursor:
            cursor.execute('SELECT password_hash FROM users WHERE user_id = %s', (session['user_id'],))
            user = cursor.fetchone()

            if not flask_bcrypt.check_password_hash(user['password_hash'], current):
                flash('Current password is wrong', 'danger')
                return redirect(url_for('change_password'))

            new_hash = flask_bcrypt.generate_password_hash(new).decode('utf-8')
            cursor.execute('UPDATE users SET password_hash = %s WHERE user_id = %s', (new_hash, session['user_id']))

        flash('Password changed', 'success')
        return redirect(url_for('profile'))

    return render_template('change_password.html')

@app.route('/logout')
def logout():
    """log out"""
    session.clear()
    return redirect(url_for('login'))