"""
Database Models for AI Sales Assistance Agent
Defines Lead, Notification, and User models
"""
from datetime import datetime

# Delay import of db to avoid circular imports
def get_db():
    """Lazily import db instance."""
    from app import db
    return db

# Get db reference for model definitions
db = None

# Will be set during app initialization
def set_db(db_instance):
    """Set the db instance for models."""
    global db
    db = db_instance


# We'll define models without inheriting from db.Model initially
# and bind them after db is initialized
class Lead:
    """Lead model for tracking potential customers (stub for imports)."""
    pass

class Notification:
    """Notification model for alerts and reminders (stub for imports)."""
    pass

class User:
    """User model for system users (stub for imports)."""
    pass


def init_models():
    """Initialize models after db is available."""
    from app import db
    
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
        role = db.Column(db.String(20), default='sales_rep')  # admin, manager, sales_rep
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        def __repr__(self):
            return f'<User {self.username}>'
    
    # Return the initialized classes
    return Lead, Notification, User
    """Lead model for tracking potential customers."""
    
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    
    # Lead characteristics for AI scoring
    source = db.Column(db.String(50), default='website')  # website, referral, cold_call, etc.
    company_size = db.Column(db.String(20), default='medium')  # small, medium, large
    engagement_level = db.Column(db.Integer, default=1)  # 1-5 scale
    budget_range = db.Column(db.String(30), default='unknown')
    timeline = db.Column(db.String(30), default='unknown')  # immediate, short_term, long_term
    
    # Status tracking
    status = db.Column(db.String(20), default='new')  # new, qualified, converted, lost
    
    # AI-generated data
    ai_score = db.Column(db.Integer, default=0)  # 0-100 score
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
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(30), default='reminder')  # reminder, alert, meeting
    priority = db.Column(db.String(20), default='normal')  # high, normal, low
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    action_date = db.Column(db.Date)
    
    def __repr__(self):
        return f'<Notification {self.title}>'
    
    def to_dict(self):
        """Convert notification to dictionary."""
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'lead_name': self.lead.name if self.lead else 'System',
            'title': self.title,
            'message': self.message,
            'notification_type': self.notification_type,
            'priority': self.priority,
            'is_read': self.is_read,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'action_date': self.action_date.strftime('%Y-%m-%d') if self.action_date else None
        }


class User(db.Model):
    """User model for sales representatives."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100))
    role = db.Column(db.String(20), default='sales_rep')  # sales_rep, manager, admin
    department = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'department': self.department,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }
    role = db.Column(db.String(30), default='sales_rep')  # admin, sales_rep, manager
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

