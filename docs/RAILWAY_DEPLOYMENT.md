# Railway Deployment Guide

Complete guide for deploying the Roofing Lead Manager to Railway with PostgreSQL and Redis.

## Overview

This guide covers:
1. Setting up Railway account
2. Deploying PostgreSQL database
3. Deploying Redis queue
4. Deploying Flask application
5. Deploying background worker
6. Configuration and testing

---

## Prerequisites

- GitHub account
- Railway account (free tier available)
- Git installed locally
- Project pushed to GitHub repository

---

## Step 1: Create Railway Account

1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Sign up with GitHub (recommended for easy deployment)
4. Verify your email address
5. Add payment method (required even for free tier)

**Free Tier Includes:**
- $5 free credit per month
- PostgreSQL database
- Redis instance
- Enough for development/small production

---

## Step 2: Create New Project

1. In Railway dashboard, click **"New Project"**
2. Select **"Empty Project"**
3. Name your project: `roofing-lead-manager`

---

## Step 3: Add PostgreSQL Database

### Provision Database

1. In your project, click **"New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway automatically provisions PostgreSQL
4. Wait for deployment to complete (~30 seconds)

### Get Database Credentials

1. Click on the **PostgreSQL** service
2. Go to **"Variables"** tab
3. You'll see these variables:
   - `DATABASE_URL` - Full connection string
   - `PGHOST` - Database host
   - `PGPORT` - Database port
   - `PGUSER` - Database user
   - `PGPASSWORD` - Database password
   - `PGDATABASE` - Database name

**Note:** You'll reference `DATABASE_URL` in your Flask app.

---

## Step 4: Add Redis

### Provision Redis

1. In your project, click **"New"**
2. Select **"Database"** → **"Add Redis"**
3. Railway automatically provisions Redis
4. Wait for deployment to complete (~30 seconds)

### Get Redis Credentials

1. Click on the **Redis** service
2. Go to **"Variables"** tab
3. You'll see:
   - `REDIS_URL` - Full connection string
   - `REDIS_HOST` - Redis host
   - `REDIS_PORT` - Redis port

**Note:** You'll reference `REDIS_URL` in your Flask app.

---

## Step 5: Deploy Flask Application

### Option A: Deploy from GitHub (Recommended)

#### Push Code to GitHub

If not already done:

```bash
cd flaskRoofingCompaniesForm-main
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/roofing-lead-manager.git
git push -u origin main
```

#### Connect to Railway

1. In Railway project, click **"New"**
2. Select **"GitHub Repo"**
3. Authorize Railway to access your GitHub
4. Select your repository
5. Railway auto-detects Python and starts building

### Option B: Deploy with Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# Deploy
railway up
```

---

## Step 6: Configure Flask App Environment Variables

1. Click on your **Flask app** service
2. Go to **"Variables"** tab
3. Click **"New Variable"** and add each:

### Required Variables

```bash
# Database - Reference PostgreSQL service
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis - Reference Redis service
REDIS_URL=${{Redis.REDIS_URL}}

# Flask Configuration
FLASK_ENV=production
FLASK_SECRET_KEY=your-random-secret-key-here-change-this

# GoHighLevel API
GHL_API_KEY=your_actual_ghl_api_key_here
GHL_API_BASE_URL=https://rest.gohighlevel.com/v1

# API Authentication
API_KEY_SALT=your-random-salt-here

# Worker Configuration
WORKER_COUNT=2

# Application Settings
MAX_CSV_SIZE_MB=10
```

### Generate Secret Keys

Use Python to generate secure random keys:

```python
import secrets
print(secrets.token_hex(32))  # For FLASK_SECRET_KEY
print(secrets.token_hex(16))  # For API_KEY_SALT
```

### Variable Reference Syntax

Railway's `${{ServiceName.VARIABLE}}` syntax automatically links services:
- `${{Postgres.DATABASE_URL}}` - References PostgreSQL connection
- `${{Redis.REDIS_URL}}` - References Redis connection

---

## Step 7: Configure Deployment Settings

### Set Start Command

1. In Flask app service, go to **"Settings"**
2. Scroll to **"Deploy"** section
3. Set **"Start Command"**:

```bash
flask db upgrade && gunicorn run:app --bind 0.0.0.0:$PORT
```

This command:
- Runs database migrations (`flask db upgrade`)
- Starts Gunicorn server
- Binds to Railway's dynamic port

### Configure Build Settings (Optional)

Railway automatically detects Python and uses the correct build process. If needed, you can customize in `railway.json`:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "flask db upgrade && gunicorn run:app --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

## Step 8: Deploy Background Worker

The worker processes leads from the Redis queue.

### Create Worker Service

1. In Railway project, click **"New"**
2. Select **"GitHub Repo"**
3. Select the **same repository** as Flask app
4. Railway creates a second service

### Configure Worker

1. Click on the new service
2. Rename it to **"Worker"**
3. Go to **"Variables"** tab
4. Add the **same environment variables** as Flask app:
   - `DATABASE_URL=${{Postgres.DATABASE_URL}}`
   - `REDIS_URL=${{Redis.REDIS_URL}}`
   - `GHL_API_KEY=your_key`
   - `FLASK_ENV=production`
   - All other variables

5. Go to **"Settings"** → **"Deploy"**
6. Set **"Start Command"**:

```bash
python worker.py
```

---

## Step 9: Verify Deployment

### Check Service Status

All services should show **"Active"** status:
- ✅ PostgreSQL
- ✅ Redis
- ✅ Flask App
- ✅ Worker

### Get Application URL

1. Click on **Flask app** service
2. Go to **"Settings"**
3. Scroll to **"Domains"**
4. Copy the Railway-provided domain (e.g., `your-app.railway.app`)

### Test Endpoints

```bash
# Health check
curl https://your-app.railway.app/health

# Redis check
curl https://your-app.railway.app/health/redis

# Register company
curl -X POST https://your-app.railway.app/company/register \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Test Company",
    "owner_name": "John Doe",
    "owner_email": "john@test.com",
    "owner_phone": "+1-555-1234",
    "ghl_location_id": "test123"
  }'
```

### Check Logs

View logs for each service:
1. Click on service
2. Go to **"Deployments"** tab
3. Click on latest deployment
4. View **"Build Logs"** and **"Deploy Logs"**

---

## Step 10: Database Migrations

Migrations run automatically on deployment via the start command. To run manually:

### Using Railway CLI

```bash
# Connect to your project
railway link

# Run migration
railway run flask db upgrade
```

### Using Railway Dashboard

1. Click on Flask app service
2. Go to **"Settings"** → **"Deploy"**
3. Temporarily change start command to:
```bash
flask db upgrade
```
4. Redeploy
5. Change back to normal start command

---

## Configuration Summary

### Project Structure on Railway

```
roofing-lead-manager (Project)
├── PostgreSQL (Database)
│   └── DATABASE_URL
├── Redis (Queue)
│   └── REDIS_URL
├── Flask App (Web Service)
│   ├── Variables: DATABASE_URL, REDIS_URL, GHL_API_KEY, etc.
│   └── Start: flask db upgrade && gunicorn run:app
└── Worker (Background Service)
    ├── Variables: Same as Flask App
    └── Start: python worker.py
```

### Environment Variables Reference

| Service | Variable | Value |
|---------|----------|-------|
| Flask App | DATABASE_URL | `${{Postgres.DATABASE_URL}}` |
| Flask App | REDIS_URL | `${{Redis.REDIS_URL}}` |
| Flask App | GHL_API_KEY | Your actual API key |
| Flask App | FLASK_SECRET_KEY | Random secret (64 chars) |
| Worker | DATABASE_URL | `${{Postgres.DATABASE_URL}}` |
| Worker | REDIS_URL | `${{Redis.REDIS_URL}}` |
| Worker | GHL_API_KEY | Your actual API key |

---

## Monitoring & Maintenance

### View Logs

**Flask App Logs:**
1. Click Flask app service
2. Go to **"Deployments"**
3. Click latest deployment
4. View logs in real-time

**Worker Logs:**
1. Click Worker service
2. Go to **"Deployments"**
3. View processing logs

### Monitor Resource Usage

1. Click on any service
2. Go to **"Metrics"** tab
3. View:
   - CPU usage
   - Memory usage
   - Network traffic

### Database Backups

Railway automatically backs up PostgreSQL:
- Daily backups retained for 7 days
- Manual backups available in dashboard

### Restart Services

If needed, restart any service:
1. Click on service
2. Go to **"Settings"**
3. Click **"Restart"**

---

## Scaling

### Vertical Scaling

Upgrade resources in Railway dashboard:
1. Click on service
2. Go to **"Settings"** → **"Resources"**
3. Adjust CPU/Memory limits

### Horizontal Scaling (Workers)

Add more worker instances:
1. Create additional worker services
2. Use same configuration
3. All workers share the same Redis queue

### Database Scaling

PostgreSQL automatically scales on Railway. For high traffic:
- Upgrade to larger database plan
- Enable connection pooling
- Add read replicas (Pro plan)

---

## Custom Domain (Optional)

### Add Custom Domain

1. Click on Flask app service
2. Go to **"Settings"** → **"Domains"**
3. Click **"Add Domain"**
4. Enter your domain (e.g., `leads.yourcompany.com`)
5. Add DNS records as shown:
   - Type: CNAME
   - Name: leads
   - Value: your-app.railway.app

### Enable HTTPS

Railway automatically provisions SSL certificates for custom domains.

---

## Troubleshooting

### App Won't Start

**Check logs:**
1. View deploy logs for errors
2. Common issues:
   - Missing environment variables
   - Database connection error
   - Port binding issue

**Solution:**
- Verify all environment variables are set
- Check DATABASE_URL format
- Ensure start command includes `--bind 0.0.0.0:$PORT`

### Database Connection Error

**Error:** `could not connect to server`

**Solution:**
1. Verify PostgreSQL service is running
2. Check DATABASE_URL is set correctly
3. Ensure using `${{Postgres.DATABASE_URL}}` syntax
4. Try restarting Flask app service

### Redis Connection Error

**Error:** `Error connecting to Redis`

**Solution:**
1. Verify Redis service is running
2. Check REDIS_URL is set correctly
3. Ensure using `${{Redis.REDIS_URL}}` syntax
4. Check worker logs for connection errors

### Worker Not Processing Jobs

**Check:**
1. Worker service is running (green status)
2. REDIS_URL is set in worker variables
3. GHL_API_KEY is configured
4. View worker logs for errors

**Solution:**
- Restart worker service
- Verify Redis connection
- Check GHL API credentials

### Migration Errors

**Error:** `relation already exists`

**Solution:**
```bash
# Connect via Railway CLI
railway link

# Reset migrations (CAUTION: destroys data)
railway run flask db downgrade base
railway run flask db upgrade
```

### Out of Memory

**Error:** `Killed` or `OOM`

**Solution:**
1. Upgrade service resources
2. Reduce WORKER_COUNT
3. Optimize database queries
4. Add pagination to large queries

---

## Cost Optimization

### Free Tier Limits

Railway free tier includes:
- $5 credit per month
- ~500 hours of usage
- Suitable for development/small production

### Reduce Costs

1. **Stop unused services** during development
2. **Reduce worker count** to 1-2 instances
3. **Use smaller database** plan if possible
4. **Monitor usage** in Railway dashboard

### Upgrade When Needed

Consider upgrading if:
- Processing >1000 leads per day
- Need 99.9% uptime
- Require more than 2 workers
- Need advanced features (backups, monitoring)

---

## Security Best Practices

### Environment Variables

- ✅ Use Railway's variable references (`${{Service.VAR}}`)
- ✅ Never commit `.env` to git
- ✅ Rotate secrets regularly
- ✅ Use strong random keys

### Database Security

- ✅ Railway handles SSL automatically
- ✅ Database is not publicly accessible
- ✅ Use strong passwords (auto-generated)
- ✅ Regular backups enabled

### Application Security

- ✅ Enable HTTPS only (Railway default)
- ✅ Set `FLASK_ENV=production`
- ✅ Implement rate limiting (future)
- ✅ Add API authentication (future)

---

## Rollback Deployment

If a deployment fails:

1. Click on Flask app service
2. Go to **"Deployments"** tab
3. Find previous working deployment
4. Click **"Redeploy"**

---

## CI/CD Pipeline

Railway automatically deploys on git push:

1. Push to GitHub main branch
2. Railway detects changes
3. Builds new image
4. Runs tests (if configured)
5. Deploys automatically
6. Runs migrations

### Disable Auto-Deploy

If you want manual control:
1. Go to service **"Settings"**
2. Scroll to **"Deploy"**
3. Disable **"Auto Deploy"**

---

## Backup & Recovery

### Database Backups

**Automatic:**
- Daily backups (7-day retention)
- Accessible in PostgreSQL service settings

**Manual Backup:**
```bash
# Using Railway CLI
railway link
railway run pg_dump $DATABASE_URL > backup.sql
```

**Restore:**
```bash
railway run psql $DATABASE_URL < backup.sql
```

### Application Backup

Your code is backed up in GitHub. To restore:
1. Revert to previous commit
2. Push to GitHub
3. Railway auto-deploys

---

## Support & Resources

### Railway Documentation
- https://docs.railway.app
- https://docs.railway.app/databases/postgresql
- https://docs.railway.app/databases/redis

### Railway Community
- Discord: https://discord.gg/railway
- GitHub: https://github.com/railwayapp

### Project Support
- Check `/health` endpoint for system status
- Review logs in Railway dashboard
- Contact system administrator

---

## Checklist

Use this checklist for deployment:

- [ ] Railway account created
- [ ] Project created
- [ ] PostgreSQL provisioned
- [ ] Redis provisioned
- [ ] Code pushed to GitHub
- [ ] Flask app deployed from GitHub
- [ ] Flask app environment variables set
- [ ] Flask app start command configured
- [ ] Worker service created
- [ ] Worker environment variables set
- [ ] Worker start command configured
- [ ] All services showing "Active" status
- [ ] Health check endpoint returns 200
- [ ] Redis health check returns healthy
- [ ] Test company registration works
- [ ] Test lead upload works
- [ ] Worker processing leads successfully
- [ ] Logs reviewed for errors
- [ ] Custom domain added (optional)

---

**Deployment Version:** 1.0  
**Last Updated:** November 2024  
**Estimated Setup Time:** 30-45 minutes
