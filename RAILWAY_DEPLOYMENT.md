# 🚂 Railway Deployment Guide

## Current Database Setup

**For Local Development:**
- **Database:** SQLite (file-based database)
- **File:** `roofing_leads.db`
- **Location:** Project root directory
- **Pros:** No setup needed, perfect for testing
- **Cons:** Not suitable for production (file-based, single connection)

**For Production (Railway):**
- **Database:** PostgreSQL
- **Managed by:** Railway
- **Pros:** Scalable, reliable, multiple connections
- **Cons:** Requires setup (but Railway makes it easy!)

---

## 🚀 Deploy to Railway - Step by Step

### Step 1: Prepare Your Project

**1.1 Create a `Procfile`** (tells Railway how to run your app)

Create a file named `Procfile` (no extension) in your project root:

```
web: gunicorn run:app
worker: python worker.py
```

**1.2 Update `requirements.txt`** (add production server)

Add this line to your `requirements.txt`:
```
gunicorn==21.2.0
```

**1.3 Create `runtime.txt`** (specify Python version)

Create a file named `runtime.txt`:
```
python-3.11.0
```

**1.4 Update `.env` for production**

Your app already reads from environment variables, so you're good!

---

### Step 2: Set Up Railway Account

1. Go to: https://railway.app
2. Click "Start a New Project"
3. Sign up with GitHub (recommended)
4. Verify your email

---

### Step 3: Create PostgreSQL Database

**In Railway Dashboard:**

1. Click **"New Project"**
2. Click **"Provision PostgreSQL"**
3. Railway will create a PostgreSQL database
4. Click on the PostgreSQL service
5. Go to **"Variables"** tab
6. You'll see: `DATABASE_URL` - Copy this!

**Example DATABASE_URL format:**
```
postgresql://user:password@host:port/database
```

---

### Step 4: Deploy Your Flask App

**Option A: Deploy from GitHub (Recommended)**

1. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/roofing-lead-manager.git
git push -u origin main
```

2. In Railway:
   - Click **"New"** → **"GitHub Repo"**
   - Select your repository
   - Railway will auto-detect it's a Python app

**Option B: Deploy from Local (Quick)**

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login:
```bash
railway login
```

3. Initialize and deploy:
```bash
railway init
railway up
```

---

### Step 5: Configure Environment Variables

**In Railway Dashboard → Your Flask App → Variables:**

Add these environment variables:

```bash
# Database (use the PostgreSQL DATABASE_URL from Step 3)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis (add Redis service first, then use this)
REDIS_URL=${{Redis.REDIS_URL}}

# GoHighLevel API
GHL_API_KEY=your_actual_ghl_api_key_here
GHL_API_BASE_URL=https://rest.gohighlevel.com/v1

# Flask
FLASK_SECRET_KEY=your_random_secret_key_here_change_this
FLASK_ENV=production

# API
API_KEY_SALT=your_random_salt_here

# Workers
WORKER_COUNT=2

# App Settings
MAX_CSV_SIZE_MB=10
```

**Important:** Railway can auto-link services using `${{ServiceName.VARIABLE}}`

---

### Step 6: Add Redis (Optional but Recommended)

1. In your Railway project, click **"New"**
2. Select **"Redis"**
3. Railway provisions Redis automatically
4. In your Flask app variables, add:
```
REDIS_URL=${{Redis.REDIS_URL}}
```

---

### Step 7: Database Migration

**Railway will automatically run migrations on deploy if you add this to your project:**

Create `railway.json` in project root:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "flask db upgrade && gunicorn run:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Or manually run migrations:**

1. In Railway Dashboard → Your App → Settings
2. Click **"Deploy"** tab
3. Add to start command:
```
flask db upgrade && gunicorn run:app
```

---

### Step 8: Enable Workers (Background Jobs)

**To run the worker process:**

1. In Railway Dashboard → Your Project
2. Click **"New"** → **"Empty Service"**
3. Name it "Worker"
4. Link it to your GitHub repo (same repo as Flask app)
5. In Settings → Start Command:
```
python worker.py
```
6. Add same environment variables as Flask app

---

## 📋 Complete Railway Setup Checklist

- [ ] Create Railway account
- [ ] Provision PostgreSQL database
- [ ] Copy DATABASE_URL
- [ ] Deploy Flask app (GitHub or CLI)
- [ ] Add environment variables
- [ ] Provision Redis (optional)
- [ ] Configure start command with migrations
- [ ] Deploy worker service (optional)
- [ ] Test the deployment
- [ ] Add custom domain (optional)

---

## 🔧 Railway Configuration Files

**Create these files in your project root:**

### 1. `Procfile`
```
web: gunicorn run:app
worker: python worker.py
```

### 2. `runtime.txt`
```
python-3.11.0
```

### 3. `railway.json` (optional but recommended)
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "flask db upgrade && gunicorn run:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 4. `.railwayignore` (optional)
```
__pycache__/
*.pyc
*.pyo
*.db
*.sqlite
*.sqlite3
.env
.env.local
venv/
.venv/
.hypothesis/
.pytest_cache/
```

---

## 🗄️ Database Comparison

| Feature | SQLite (Local) | PostgreSQL (Railway) |
|---------|----------------|---------------------|
| Setup | None needed | Automatic on Railway |
| File | `roofing_leads.db` | Hosted by Railway |
| Connections | Single | Multiple |
| Scalability | Limited | High |
| Backups | Manual | Automatic |
| Cost | Free | Free tier available |
| Best For | Development | Production |

---

## 🔄 Switching from SQLite to PostgreSQL

**Your app already supports both!** Just change the `DATABASE_URL`:

**Local (SQLite):**
```
DATABASE_URL=sqlite:///roofing_leads.db
```

**Production (PostgreSQL):**
```
DATABASE_URL=postgresql://user:password@host:port/database
```

The app automatically detects which database to use based on the URL format!

---

## 🧪 Test Your Deployment

After deploying to Railway:

1. **Get your app URL:**
   - Railway Dashboard → Your App → Settings
   - Copy the domain (e.g., `your-app.railway.app`)

2. **Test endpoints:**
```bash
# Health check
curl https://your-app.railway.app/health

# Register company
curl -X POST https://your-app.railway.app/company/register \
  -H "Content-Type: application/json" \
  -d '{"company_name":"Test Co","owner_name":"John","owner_email":"john@test.com","owner_phone":"+1-555-1234","ghl_location_id":"test"}'
```

3. **Open in browser:**
```
https://your-app.railway.app
```

---

## 💰 Railway Pricing

**Free Tier:**
- $5 free credit per month
- Enough for small projects
- PostgreSQL included
- Redis included

**Pro Plan:**
- $20/month
- More resources
- Better for production

---

## 🆘 Troubleshooting

**App won't start:**
- Check logs in Railway Dashboard
- Verify all environment variables are set
- Make sure `DATABASE_URL` is correct

**Database connection error:**
- Verify PostgreSQL service is running
- Check `DATABASE_URL` format
- Ensure app and database are in same project

**Worker not processing:**
- Check Redis is provisioned
- Verify `REDIS_URL` is set
- Check worker logs

**Migrations not running:**
- Add `flask db upgrade` to start command
- Or run manually in Railway CLI

---

## 📚 Useful Railway Commands

```bash
# Login
railway login

# Link to project
railway link

# View logs
railway logs

# Run command
railway run python manage.py

# Open app in browser
railway open

# Check status
railway status
```

---

## ✅ Quick Start Summary

1. **Create Railway account** → https://railway.app
2. **Provision PostgreSQL** → Copy DATABASE_URL
3. **Deploy app** → Connect GitHub or use CLI
4. **Set variables** → Add DATABASE_URL and others
5. **Add Redis** → Optional but recommended
6. **Deploy worker** → For background jobs
7. **Test** → Visit your-app.railway.app

**Your app is already configured to work with PostgreSQL! Just deploy and set the DATABASE_URL! 🚀**
