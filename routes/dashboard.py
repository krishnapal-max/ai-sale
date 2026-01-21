"""
Dashboard Routes
Main dashboard with analytics and overview
"""
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from database.models import Lead, Notification
from database.db_instance import db
from ai import lead_scorer
from ai.recommendation import recommendation_engine
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)

def login_required(f):
    """Decorator to require login."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@dashboard_bp.route('/')
@login_required
def index():
    """Main dashboard view."""
    # Get lead statistics
    total_leads = Lead.query.count()
    
    # Status counts
    status_counts = db.session.query(
        Lead.status, func.count(Lead.id)
    ).group_by(Lead.status).all()
    status_dict = {status: count for status, count in status_counts}
    
    # Priority counts
    high_priority = Lead.query.filter(Lead.ai_score >= 70).count()
    medium_priority = Lead.query.filter(
        Lead.ai_score >= 40, Lead.ai_score < 70
    ).count()
    low_priority = Lead.query.filter(Lead.ai_score < 40).count()
    
    # Recent leads
    recent_leads = Lead.query.order_by(Lead.created_at.desc()).limit(5).all()
    
    # High priority leads
    top_leads = Lead.query.filter(Lead.ai_score >= 70).order_by(
        Lead.ai_score.desc()
    ).limit(5).all()
    
    # Unread notifications
    unread_notifications = Notification.query.filter(
        Notification.is_read == False
    ).order_by(Notification.created_at.desc()).limit(5).all()
    
    # Recommendation summary
    recommendations = recommendation_engine.get_bulk_recommendations()
    
    return render_template(
        'dashboard.html',
        title='Dashboard - AI Sales Agent',
        total_leads=total_leads,
        status_counts=status_dict,
        high_priority=high_priority,
        medium_priority=medium_priority,
        low_priority=low_priority,
        recent_leads=recent_leads,
        top_leads=top_leads,
        notifications=unread_notifications,
        recommendation_count=len(recommendations)
    )

@dashboard_bp.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics."""
    total_leads = Lead.query.count()
    
    status_counts = db.session.query(
        Lead.status, func.count(Lead.id)
    ).group_by(Lead.status).all()
    
    high_priority = Lead.query.filter(Lead.ai_score >= 70).count()
    medium_priority = Lead.query.filter(
        Lead.ai_score >= 40, Lead.ai_score < 70
    ).count()
    low_priority = Lead.query.filter(Lead.ai_score < 40).count()
    
    unread_notifications = Notification.query.filter(
        Notification.is_read == False
    ).count()
    
    return jsonify({
        'total_leads': total_leads,
        'status_counts': dict(status_counts),
        'priority_counts': {
            'high': high_priority,
            'medium': medium_priority,
            'low': low_priority
        },
        'unread_notifications': unread_notifications
    })

@dashboard_bp.route('/api/recommendations')
def api_recommendations():
    """API endpoint for recommendations."""
    recommendations = recommendation_engine.get_bulk_recommendations()
    return jsonify(recommendations)

@dashboard_bp.route('/api/report')
def api_report():
    """API endpoint for recommendation report."""
    report = recommendation_engine.generate_report()
    return jsonify(report)

