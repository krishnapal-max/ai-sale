"""
Authentication Routes
Handles user login, logout, and registration
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.db_instance import db
from database.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.before_request
def before_request():
    """Check if user is logged in before each request."""
    if 'user_id' in session:
        from database.models import User
        user = User.query.get(session['user_id'])
        if user and user.is_active:
            # User is logged in and active
            pass
        else:
            session.clear()
    
    # Pass logged-in status to templates
    from flask import g
    g.logged_in = 'user_id' in session
    if g.logged_in:
        g.user = User.query.get(session['user_id'])


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page and handler."""
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            session['user_id'] = user.id
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page and handler."""
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # Validation
        if not all([username, email, password, password_confirm]):
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if password != password_confirm:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration', 'error')
    
    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    """Logout the current user."""
    username = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        username = user.username if user else 'User'
    
    session.clear()
    flash(f'Goodbye! You have been logged out.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
def profile():
    """User profile page."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
    
    return render_template('profile.html', user=user)


def login_required(f):
    """Decorator to require login for a route."""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('auth.login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_active:
            session.clear()
            flash('Your account is no longer active', 'error')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    
    return decorated_function
