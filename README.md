# 🤖 AI Sales Assistance Agent

An intelligent Flask-based web application for sales teams that uses machine learning to automatically score leads and provide AI-powered recommendations.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.2-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

- **🎯 AI Lead Scoring**: Random Forest ML model scores leads automatically based on multiple factors
- **📊 Dashboard**: Real-time analytics and lead statistics
- **👥 Lead Management**: Full CRUD operations for leads and prospects
- **💡 Smart Recommendations**: AI-powered action suggestions for each lead
- **🔔 Notifications**: Automated reminders and alerts for sales follow-ups
- **🤖 Chatbot Assistant**: AI-powered help and guidance system
- **🌙 Dark Mode**: Beautiful dark/light theme support
- **📱 Responsive Design**: Works on desktop, tablet, and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ai-sales-agent.git
cd ai-sales-agent
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Access the app**
- Open http://localhost:5000
- **Demo Login**: `admin` / `admin123` or `demo` / `demo123`

## 📁 Project Structure

```
ai-sales-agent/
├── ai/                    # AI/ML module
│   ├── lead_scoring.py   # Lead scoring model
│   └── recommendation.py  # Recommendation engine
├── database/             # Database models & setup
│   ├── models.py        # SQLAlchemy models
│   └── db_setup.py      # Database initialization
├── routes/              # Flask blueprints
│   ├── auth.py         # Authentication
│   ├── leads.py        # Lead management
│   ├── dashboard.py    # Dashboard
│   ├── notifications.py # Notifications
│   └── chatbot.py      # Chatbot routes
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── config.py           # Configuration
├── app.py              # Main application
└── requirements.txt    # Dependencies
```

## 🤖 AI Scoring Model

The ML model considers:
- Lead source (website, referral, cold call)
- Company size (small, medium, large)
- Engagement level (1-5 scale)
- Budget range (low, medium, high)
- Sales timeline (immediate, short-term, long-term)

**Score Ranges:**
- 🔴 **High Priority**: 70-100
- 🟡 **Medium Priority**: 40-69
- 🟢 **Low Priority**: 0-39

## 📦 Tech Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLite (SQLAlchemy ORM)
- **ML**: scikit-learn (Random Forest)
- **Data**: pandas, numpy
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Gunicorn

## 🌐 Deploy to Free Hosting

### Railway (Recommended)
1. Connect GitHub repo to [Railway.app](https://railway.app)
2. Set environment: `FLASK_ENV=production`
3. Deploy automatically on push

### Render
1. Connect GitHub to [Render.com](https://render.com)
2. Build Command: `pip install -r requirements-prod.txt`
3. Start Command: `gunicorn app:app`

### Other Options
- **Heroku**: Using alternative platforms (Heroku free tier ended)
- **PythonAnywhere**: Free Python hosting with limitations
- **Replit**: Code + deploy in browser

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📊 Sample Data

Seed the database with sample leads:
```bash
python seed_data.py
```

## 🔑 Default Users

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator |
| demo | demo123 | Sales Rep |

## 📝 Features in Detail

### Lead Scoring
- Automatic ML scoring on lead creation/update
- Re-score any lead with AI algorithm
- Batch scoring for multiple leads

### Dashboard
- Total leads overview
- Priority-based statistics
- Recent activity feed
- Top opportunities
- Unread notifications

### Lead Management
- Add, edit, view, delete leads
- Filter by status and priority
- Export leads to CSV
- Lead detail view with scoring breakdown

### Notifications
- Automated reminders
- Manual notification generation
- Mark as read/unread
- Filter by type

### AI Recommendations
- Call scheduling suggestions
- Email templates
- Follow-up recommendations
- Conversion probability

## 🐛 Troubleshooting

**App won't start:**
```bash
# Check Python version
python --version  # Should be 3.10+

# Verify dependencies
pip list

# Check database
ls data/sales_agent.db
```

**Database issues:**
```bash
# Reset database (delete and recreate)
rm data/sales_agent.db
python app.py  # Recreates DB
```

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 👨‍💻 Author

**AI Sales Agent**
- GitHub: [@your-username](https://github.com/your-username)

## 📞 Support

For support, email: [support@salesagent.com](mailto:support@salesagent.com) or open an issue on GitHub.

## 🎯 Roadmap

- [ ] REST API with authentication
- [ ] Mobile app (React Native)
- [ ] Advanced analytics with charts
- [ ] Email integration
- [ ] SMS notifications
- [ ] CRM synchronization
- [ ] Custom ML model training

---

**⭐ If you find this helpful, please star the repository!**
