"""
AI Sales Assistance Agent - Main Application
Flask-based web application for sales team automation
"""
from flask import Flask, session
from database.db_instance import db
from config import config

def create_app(config_name='development'):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    with app.app_context():
        # Import models to register them with db
        from database.models import Lead, Notification, User
        
        # Create database tables
        db.create_all()
        
        # Create default admin user if none exists
        if User.query.filter_by(username='admin').first() is None:
            admin = User(username='admin', email='admin@salesagent.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Create demo user
            demo = User(username='demo', email='demo@salesagent.com', role='sales_rep')
            demo.set_password('demo123')
            db.session.add(demo)
            
            db.session.commit()
            print("✅ Default users created (admin/admin123, demo/demo123)")
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.chatbot import chatbot_bp
    from routes.leads import leads_bp
    from routes.dashboard import dashboard_bp
    from routes.notifications import notifications_bp
    from routes.help_assistant import help_assistant_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    app.register_blueprint(leads_bp, url_prefix='/leads')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
    app.register_blueprint(help_assistant_bp, url_prefix='/help')
    
    # Redirect root to login or dashboard
    @app.route('/')
    def index():
        from flask import redirect, url_for
        if 'user_id' in session:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))
    
    return app

# Create application instance for Flask to use
app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("🤖 AI SALES ASSISTANCE AGENT")
    print("=" * 60)
    print("Starting application...")
    print("Access the dashboard at: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True)

