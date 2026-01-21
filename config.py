"""
AI Sales Assistance Agent - Configuration Module
"""
import os

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-ai-sales-agent'
    DEBUG = True
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Database configuration (SQLite for simplicity)
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data', 'sales_agent.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Model settings
    AI_MODEL_PATH = os.path.join(basedir, 'ai', 'model')
    AI_SCORE_THRESHOLDS = {
        'high': 70,      # Score >= 70: High priority
        'medium': 40,    # Score >= 40: Medium priority
        'low': 0         # Score < 40: Low priority
    }
    
    # Notification settings
    NOTIFICATION_REMINDER_DAYS = 3
    HIGH_PRIORITY_THRESHOLD = 70

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.basedir, 'data', 'sales_agent.db')

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Use PostgreSQL or MySQL in production
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

