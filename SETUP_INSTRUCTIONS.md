# AI Sales Assistance Agent - Setup & Run Instructions

## Project Overview
A Flask-based AI sales assistance agent that uses machine learning to score leads and provide automated recommendations for sales teams.

## ✅ What Was Fixed & Created

### 1. **Dependencies Installation**
- Installed all required Python packages from `requirements.txt`:
  - Flask, Flask-SQLAlchemy, scikit-learn, pandas, numpy, python-dateutil, werkzeug

### 2. **Python Code Fixes**
- **ai/__init__.py**: Fixed ML model training with proper numeric encoding instead of string arrays
- **routes/leads.py**: Fixed import statement from `ai.lead_scoring` to `ai` 
- **routes/dashboard.py**: Fixed import statement to use correct module path
- **data/sample_data.py**: Fixed import statements and verified completeness
- **ai/recommendation.py**: Fixed dictionary entries with missing 'icon' keys
- **database/db_setup.py**: Completed User model with all required fields and methods

### 3. **Template Fixes**
- **templates/lead_detail.html**: Refactored Jinja2 variable assignments to avoid CSS linter errors
- **templates/lead_form.html**: Fixed inline style Jinja2 expressions
- **templates/dashboard.html**: Moved Jinja2 variables out of inline styles, added CSS class-based coloring
- **templates/leads.html**: Fixed onclick handler escaping for rescoreLead function

### 4. **Module Structure**
- Created `data/__init__.py` for the data module
- Verified all `__init__.py` files in packages are properly configured

### 5. **Configuration**
- Python environment configured with virtual environment
- All dependencies installed and verified

## 🚀 How to Run the Application

### Prerequisites
- Python 3.10+
- Virtual environment (already configured)

### Installation & Startup

```bash
# Navigate to the project directory
cd "/home/krishna/Downloads/ai project"

# Run the application
.venv/bin/python app.py
```

The application will:
1. Load or train the AI model
2. Create database tables automatically
3. Start the Flask development server
4. Be accessible at `http://localhost:5000`

### Accessing Features
- **Dashboard**: Home page with lead statistics and overview
- **Lead Management**: View, create, edit, and delete leads
- **Lead Scoring**: AI automatically scores leads when added/updated
- **Recommendations**: View AI-generated action recommendations
- **Notifications**: Track follow-up reminders and alerts

## 📊 Database Models

### Lead Model
- Stores lead information with AI scoring data
- Tracks lead status, source, company details
- Stores AI score and recommended actions
- Manages follow-up scheduling

### Notification Model
- Tracks alerts, reminders, and notifications
- Links to specific leads
- Supports different priority levels

### User Model
- Manages sales representatives
- Supports different roles (sales_rep, manager, admin)

## 🤖 AI Scoring System

The system uses:
1. **Machine Learning**: Random Forest classifier trained on sample data
2. **Feature Encoding**: Numeric encoding of categorical features
3. **Fallback Scoring**: Rule-based scoring when ML is unavailable

### Scoring Factors
- **Lead Source** (Referral, LinkedIn, Website, Cold Call)
- **Company Size** (Small, Medium, Large, Enterprise)
- **Engagement Level** (1-5 scale)
- **Budget Range** (Unknown, Low, Medium, High, Enterprise)
- **Sales Timeline** (Immediate, Short-term, Long-term, Unknown)

## 📝 API Endpoints

### Dashboard
- `GET /` - Main dashboard
- `GET /api/stats` - Dashboard statistics
- `GET /api/recommendations` - Bulk recommendations
- `GET /api/report` - Recommendation report

### Leads
- `GET /leads/` - List all leads
- `GET /leads/add` - Add lead form
- `POST /leads/add` - Create new lead
- `GET /leads/edit/<id>` - Edit lead form
- `POST /leads/edit/<id>` - Update lead
- `GET /leads/delete/<id>` - Delete lead
- `GET /leads/view/<id>` - View lead details
- `GET /leads/score/<id>` - Re-score lead
- `GET /leads/status/<id>/<status>` - Update lead status
- `GET /leads/batch-score` - Score all leads
- `GET /leads/api/lead/<id>` - Get lead as JSON
- `GET /leads/api/score/<id>` - Score lead API

### Notifications
- `GET /notifications/` - List all notifications
- `GET /notifications/unread` - List unread notifications
- `GET /notifications/mark-read/<id>` - Mark notification as read
- `GET /notifications/mark-all-read` - Mark all as read
- `GET /notifications/delete/<id>` - Delete notification
- `POST /notifications/create` - Create notification
- `GET /notifications/generate-reminders` - Generate follow-up reminders
- `GET /notifications/api/count` - Get unread count
- `GET /notifications/api/recent` - Get recent notifications

## 🔧 Configuration

See `config.py` for:
- Flask settings
- Database configuration (SQLite)
- AI model settings
- Score thresholds and notification settings

## 📁 Project Structure

```
ai project/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── ai/
│   ├── __init__.py        # AI scoring module
│   └── recommendation.py   # Recommendation engine
├── database/
│   ├── __init__.py        # Database initialization
│   └── db_setup.py        # Database models
├── routes/
│   ├── __init__.py        # Routes package
│   ├── dashboard.py       # Dashboard routes
│   ├── leads.py           # Lead routes
│   └── notifications.py   # Notification routes
├── templates/
│   ├── base.html          # Base template
│   ├── dashboard.html     # Dashboard template
│   ├── leads.html         # Leads list template
│   ├── lead_form.html     # Lead form template
│   ├── lead_detail.html   # Lead detail template
│   └── notifications.html # Notifications template
├── static/
│   ├── css/
│   │   └── style.css      # Stylesheet
│   └── js/
│       └── main.js        # JavaScript functions
├── data/
│   ├── __init__.py        # Data module
│   └── sample_data.py     # Sample data generator
└── TODO.md                # Project todo list
```

## ✨ Features

✅ **Lead Management**: Create, read, update, delete leads
✅ **AI Scoring**: Automatic lead scoring with ML model
✅ **Recommendations**: AI-generated action recommendations
✅ **Notifications**: Follow-up reminders and alerts
✅ **Dashboard**: Real-time statistics and analytics
✅ **Status Tracking**: Track lead status through pipeline
✅ **Batch Operations**: Score multiple leads at once
✅ **API Endpoints**: JSON API for frontend integration

## 🧪 Testing

To test the application:

```bash
# Import the app to verify it loads correctly
.venv/bin/python -c "import app; print('✅ App imports successfully')"

# Run the app with debug mode
.venv/bin/python app.py
```

## 📚 Next Steps

1. **Add Sample Data**: Use `data/sample_data.py` to populate database with test leads
2. **Customize Scoring**: Adjust thresholds and rules in `ai/__init__.py` and `ai/recommendation.py`
3. **Deploy**: Use a production WSGI server (Gunicorn, uWSGI) for deployment
4. **Integration**: Connect to CRM systems or sales tools

---

**Status**: ✅ All fixes completed and application ready to run!
