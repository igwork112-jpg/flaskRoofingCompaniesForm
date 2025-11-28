# 🗄️ Database Information

## Current Setup (Local Development)

**Database:** SQLite
**File:** `roofing_leads.db`
**Location:** Project root directory

### Why SQLite for Local?
✅ No setup required
✅ Perfect for testing
✅ File-based (easy to delete and restart)
✅ Works on Windows without issues

### Tables Created:
1. **company_profiles** - Stores roofing companies
2. **leads** - Stores all leads
3. **lead_processing_logs** - Tracks processing status

---

## Production Setup (Railway)

**Database:** PostgreSQL
**Managed by:** Railway (automatic provisioning)

### Why PostgreSQL for Production?
✅ Scalable (handles many connections)
✅ Reliable (automatic backups)
✅ Industry standard
✅ Free tier on Railway

---

## Your App Supports Both!

Your application is **already configured** to work with both databases!

**It automatically detects which database to use based on the `DATABASE_URL`:**

**SQLite (Local):**
```
DATABASE_URL=sqlite:///roofing_leads.db
```

**PostgreSQL (Railway):**
```
DATABASE_URL=postgresql://user:password@host:port/database
```

No code changes needed! Just change the environment variable!

---

## Railway Setup - Quick Version

### 1. Create Railway Account
Go to: https://railway.app

### 2. Provision PostgreSQL
- Click "New Project"
- Click "Provision PostgreSQL"
- Copy the `DATABASE_URL`

### 3. Deploy Your App
- Connect your GitHub repo
- Or use Railway CLI: `railway up`

### 4. Set Environment Variables
In Railway Dashboard → Variables:
```
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
GHL_API_KEY=your_key_here
FLASK_SECRET_KEY=random_secret_here
FLASK_ENV=production
```

### 5. Done!
Your app will automatically:
- Connect to PostgreSQL
- Create all tables
- Start accepting requests

---

## Files Created for Railway

✅ `Procfile` - Tells Railway how to run your app
✅ `runtime.txt` - Specifies Python version
✅ `railway.json` - Deployment configuration
✅ `requirements.txt` - Updated with gunicorn & psycopg2

**Everything is ready for deployment!**

---

## Database Schema (Same for Both)

### company_profiles
```sql
id, company_name, owner_name, owner_phone, 
owner_email, ghl_location_id, created_at, updated_at
```

### leads
```sql
id, company_id, name, phone, notes, created_at
```

### lead_processing_logs
```sql
id, lead_id, company_id, status, worker_id, 
ghl_contact_id, error_message, attempt_count, 
created_at, updated_at
```

---

## Migration Commands

**Create migration:**
```bash
flask db migrate -m "Description"
```

**Apply migration:**
```bash
flask db upgrade
```

**Rollback:**
```bash
flask db downgrade
```

**Railway automatically runs migrations on deploy!**

---

## Testing Both Databases

**Test SQLite (Local):**
```bash
# Already working!
python run.py
```

**Test PostgreSQL (Local):**
```bash
# Install PostgreSQL locally
# Update .env with PostgreSQL URL
DATABASE_URL=postgresql://localhost/roofing_leads
python run.py
```

**Test on Railway:**
```bash
# After deployment
curl https://your-app.railway.app/health
```

---

## Data Migration (SQLite → PostgreSQL)

If you want to move your local data to Railway:

**Option 1: Export/Import CSV**
1. Export from SQLite to CSV
2. Upload via your CSV upload form

**Option 2: Database Dump**
1. Use `sqlite3` to export
2. Convert to PostgreSQL format
3. Import to Railway database

**Option 3: Start Fresh**
- Just deploy and start adding data
- Recommended for testing

---

## Summary

**Current Database:** SQLite (`roofing_leads.db`)

**Production Database:** PostgreSQL (on Railway)

**Your App:** Already supports both! 🎉

**To Deploy:** Follow `RAILWAY_DEPLOYMENT.md`

**No code changes needed!** Just set the `DATABASE_URL` environment variable!
