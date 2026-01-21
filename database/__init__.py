"""
Database Setup Module
Handles database initialization and migrations
"""
from datetime import datetime

# Note: db instance is created in app.py and imported here
# This avoids creating multiple SQLAlchemy instances

def init_db(app):
    """Initialize database with the Flask app."""
    from app import db
    db.init_app(app)

def create_tables():
    """Create all database tables."""
    from app import db
    db.create_all()
    print("✅ Database tables created successfully!")

def drop_tables():
    """Drop all database tables (use with caution)."""
    from app import db
    db.drop_all()
    print("⚠️ All database tables dropped!")

