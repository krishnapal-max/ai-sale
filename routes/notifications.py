"""
Notification Routes
Handles notifications and reminders
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from database.models import Notification, Lead
from database.db_instance import db
from datetime import datetime, timedelta
from functools import wraps

notifications_bp = Blueprint('notifications', __name__)

def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@notifications_bp.route('/')
@login_required
def index():
    """List all notifications."""
    notifications = Notification.query.order_by(
        Notification.created_at.desc()
    ).all()
    
    return render_template(
        'notifications.html',
        notifications=notifications,
        title='Notifications'
    )

@notifications_bp.route('/unread')
@login_required
def unread():
    """Show only unread notifications."""
    notifications = Notification.query.filter(
        Notification.is_read == False
    ).order_by(Notification.created_at.desc()).all()
    
    return render_template(
        'notifications.html',
        notifications=notifications,
        title='Unread Notifications'
    )

@notifications_bp.route('/mark-read/<int:id>')
@login_required
def mark_read(id):
    """Mark a notification as read."""
    notification = Notification.query.get_or_404(id)
    notification.is_read = True
    db.session.commit()
    
    flash('Notification marked as read', 'success')
    return redirect(url_for('notifications.index'))

@notifications_bp.route('/mark-all-read')
@login_required
def mark_all_read():
    """Mark all notifications as read."""
    Notification.query.update({Notification.is_read: True})
    db.session.commit()
    
    flash('All notifications marked as read', 'success')
    return redirect(url_for('notifications.index'))

@notifications_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    """Delete a notification."""
    notification = Notification.query.get_or_404(id)
    db.session.delete(notification)
    db.session.commit()
    
    flash('Notification deleted', 'success')
    return redirect(url_for('notifications.index'))

@notifications_bp.route('/create', methods=['POST'])
@login_required
def create():
    """Create a new notification."""
    try:
        notification = Notification(
            lead_id=request.form.get('lead_id'),
            title=request.form['title'],
            message=request.form['message'],
            notification_type=request.form.get('type', 'reminder'),
            priority=request.form.get('priority', 'normal'),
            action_date=request.form.get('action_date')
        )
        
        db.session.add(notification)
        db.session.commit()
        
        flash('Notification created successfully', 'success')
    except Exception as e:
        flash(f'Error creating notification: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('notifications.index'))

@notifications_bp.route('/generate-reminders')
@login_required
def generate_reminders():
    """Generate follow-up reminders for leads."""
    today = datetime.utcnow().date()
    
    # Find leads that need follow-up
    leads = Lead.query.filter(
        Lead.next_followup <= today,
        Lead.status.in_(['new', 'qualified'])
    ).all()
    
    created_count = 0
    for lead in leads:
        # Check if there's already a notification for this lead
        existing = Notification.query.filter(
            Notification.lead_id == lead.id,
            Notification.notification_type == 'reminder',
            Notification.is_read == False
        ).first()
        
        if not existing:
            notification = Notification(
                lead_id=lead.id,
                title=f"Follow-up Reminder: {lead.name}",
                message=f"It's time to follow up with {lead.name} from {lead.company}",
                notification_type='reminder',
                priority='normal',
                action_date=today + timedelta(days=1)
            )
            db.session.add(notification)
            created_count += 1
    
    db.session.commit()
    flash(f'Generated {created_count} follow-up reminders', 'success')
    return redirect(url_for('notifications.index'))

@notifications_bp.route('/api/count')
def api_count():
    """API endpoint to get unread notification count."""
    count = Notification.query.filter(Notification.is_read == False).count()
    return jsonify({'count': count})

@notifications_bp.route('/api/recent')
def api_recent():
    """API endpoint to get recent notifications."""
    notifications = Notification.query.filter(
        Notification.is_read == False
    ).order_by(Notification.created_at.desc()).limit(5).all()
    
    return jsonify([n.to_dict() for n in notifications])

