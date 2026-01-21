# AI Sales Assistance Agent - Deployment Guide

## Deploying to Free Hosting Platforms

### Option 1: Railway (Recommended - Easiest)
1. **Create Railway Account**: https://railway.app
2. **Connect GitHub**: Link your GitHub account
3. **Create New Project** → Deploy from GitHub repo
4. **Environment Variables**: Set `FLASK_ENV=production`
5. **Database**: Railway auto-creates PostgreSQL for free tier

### Option 2: Render
1. **Create Render Account**: https://render.com
2. **New Web Service** → Connect GitHub
3. **Configuration**:
   - Build Command: `pip install -r requirements-prod.txt`
   - Start Command: `gunicorn app:app`
   - Environment: `FLASK_ENV=production`
4. **Database**: Use Render's free PostgreSQL

### Option 3: Heroku Alternative (if you want traditional Heroku setup)
Note: Heroku free tier ended, but you can use Railway/Render as replacement

## Steps to Deploy

### 1. Initialize Git & Push to GitHub

```bash
cd "/home/krishna/Downloads/ai project"

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI Sales Assistant Agent"

# Add GitHub remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/ai-sales-agent.git
git branch -M main
git push -u origin main
```

### 2. Production Config Updates

Update `config.py`:
```python
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///sales_agent.db')
```

### 3. Deploy Command (Example for Railway)

```bash
# Railway CLI: railway deploy
```

## Environment Variables for Production

Set these on your hosting platform:
- `FLASK_ENV=production`
- `SECRET_KEY=your-secure-random-key`
- `DATABASE_URL=your-database-url` (if using external DB)

## Free Tier Limitations

| Platform | Free Tier | Notes |
|----------|-----------|-------|
| Railway | $5/month | Plenty for small apps |
| Render | Always Free | 0.5GB RAM, auto-sleeps |
| PythonAnywhere | Free | Limited hours/month |

