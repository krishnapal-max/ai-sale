"""
Database Models for AI Sales Assistance Agent
Defines Lead, Notification, and User models
"""
from datetime import datetime
from database.db_instance import db
from werkzeug.security import generate_password_hash, check_password_hash


class Lead(db.Model):
    """Lead model for tracking potential customers."""
    
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    
    # Lead characteristics for AI scoring
    source = db.Column(db.String(50), default='website')
    company_size = db.Column(db.String(20), default='medium')
    engagement_level = db.Column(db.Integer, default=1)
    budget_range = db.Column(db.String(30), default='unknown')
    timeline = db.Column(db.String(30), default='unknown')
    
    # Status tracking
    status = db.Column(db.String(20), default='new')
    
    # AI-generated data
    ai_score = db.Column(db.Integer, default=0)
    recommended_action = db.Column(db.String(100))
    last_contacted = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    next_followup = db.Column(db.Date)
    
    # Relationships
    notifications = db.relationship('Notification', backref='lead', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Lead {self.name} - Score: {self.ai_score}>'
    
    def to_dict(self):
        """Convert lead to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'job_title': self.job_title,
            'source': self.source,
            'company_size': self.company_size,
            'engagement_level': self.engagement_level,
            'budget_range': self.budget_range,
            'timeline': self.timeline,
            'status': self.status,
            'ai_score': self.ai_score,
            'recommended_action': self.recommended_action,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M'),
            'next_followup': self.next_followup.strftime('%Y-%m-%d') if self.next_followup else None
        }
    
    def get_priority(self):
        """Get priority level based on AI score."""
        if self.ai_score >= 70:
            return 'high'
        elif self.ai_score >= 40:
            return 'medium'
        else:
            return 'low'


class Notification(db.Model):
    """Notification model for alerts and reminders."""
    
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False)
    type = db.Column(db.String(50))  # reminder, alert, suggestion, meeting
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    is_read = db.Column(db.Boolean, default=False)
    action_required = db.Column(db.Boolean, default=False)
    action_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Notification {self.title}>'
    
    def to_dict(self):
        """Convert notification to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'priority': self.priority,
            'is_read': self.is_read,
            'action_required': self.action_required,
            'action_url': self.action_url,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'expires_at': self.expires_at.strftime('%Y-%m-%d %H:%M') if self.expires_at else None
        }


class User(db.Model):
    """User model for system users."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='sales_rep')  # admin, manager, sales_rep
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set the password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
