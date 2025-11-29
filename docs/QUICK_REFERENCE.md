# Quick Reference Guide

Essential commands and endpoints for daily use.

## Local Development

### Start Services

```bash
# Terminal 1: Start Flask app
python run.py

# Terminal 2: Start Redis (Docker)
docker run -d -p 6379:6379 redis

# Terminal 3: Start worker
python worker.py
```

### Access Application

- **Web UI**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **Redis Status**: http://localhost:5000/health/redis

---

## Essential API Endpoints

### Health Checks

```bash
# System health
curl http://localhost:5000/health

# Redis status
curl http://localhost:5000/health/redis
```

### Register Company

```bash
curl -X POST http://localhost:5000/company/register \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "ABC Roofing",
    "owner_name": "John Doe",
    "owner_email": "john@example.com",
    "owner_phone": "+1-555-1234",
    "ghl_location_id": "your_location_id"
  }'
```

### Upload Single Lead

```bash
curl -X POST http://localhost:5000/leads/single \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "phone": "+1-555-5678",
    "notes": "Interested in roof repair",
    "company_id": 1
  }'
```

### Bulk Upload

```bash
curl -X POST http://localhost:5000/api/leads/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "leads": [
      {
        "name": "John Doe",
        "phone": "+1-555-1234",
        "company_id": 1
      }
    ]
  }'
```

---

## Database Commands

### Migrations

```bash
# Create migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback
flask db downgrade
```

### Direct Database Access

```bash
# SQLite (local)
sqlite3 instance/roofing_leads.db

# PostgreSQL (Railway)
railway run psql $DATABASE_URL
```

---

## Redis Commands

### Check Redis

```bash
# Ping Redis
redis-cli ping

# Check queue length
redis-cli LLEN rq:queue:lead_processing

# View all keys
redis-cli KEYS "*"
```

---

## Railway Commands

### Deploy

```bash
# Install CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up

# View logs
railway logs

# Run command
railway run flask db upgrade
```

---

## Environment Variables

### Local (.env)

```bash
FLASK_ENV=development
DATABASE_URL=sqlite:///roofing_leads.db
REDIS_URL=redis://localhost:6379/0
GHL_API_KEY=your_key_here
```

### Production (Railway)

```bash
FLASK_ENV=production
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
GHL_API_KEY=your_key_here
FLASK_SECRET_KEY=random_secret_key
```

---

## Troubleshooting

### Redis Not Running

```bash
# Check if Redis is running
redis-cli ping

# Start Redis (Docker)
docker run -d -p 6379:6379 redis

# Check health endpoint
curl http://localhost:5000/health/redis
```

### Database Issues

```bash
# Reset database (CAUTION: destroys data)
rm instance/roofing_leads.db
flask db upgrade

# Check database connection
python -c "from app.app import create_app; app = create_app(); print('OK')"
```

### Worker Not Processing

```bash
# Check worker is running
ps aux | grep worker.py

# Restart worker
pkill -f worker.py
python worker.py

# Check Redis queue
redis-cli LLEN rq:queue:lead_processing
```

---

## Common Tasks

### Add New Company

1. Go to http://localhost:5000/register-company
2. Fill in form
3. Submit
4. Note the company_id from response

### Upload Leads

**Via Web UI:**
1. Go to http://localhost:5000/add-lead
2. Select company
3. Enter lead details
4. Submit

**Via CSV:**
1. Create CSV with columns: name, phone, notes
2. Go to http://localhost:5000/upload-csv
3. Select company and file
4. Upload

**Via API:**
```bash
curl -X POST http://localhost:5000/api/leads/bulk \
  -H "Content-Type: application/json" \
  -d @leads.json
```

### Monitor Processing

1. Go to http://localhost:5000/dashboard
2. View company statistics
3. Check success/failure rates

---

## File Locations

### Configuration
- `.env` - Local environment variables
- `config.py` - Application configuration

### Application
- `run.py` - Application entry point
- `worker.py` - Background worker
- `app/` - Application code

### Database
- `instance/roofing_leads.db` - SQLite database (local)
- Migrations in `migrations/` (auto-generated)

### Documentation
- `README.md` - Project overview
- `docs/API_REFERENCE.md` - API documentation
- `docs/RAILWAY_DEPLOYMENT.md` - Deployment guide

---

## Port Reference

| Service | Port | URL |
|---------|------|-----|
| Flask | 5000 | http://localhost:5000 |
| Redis | 6379 | redis://localhost:6379 |
| PostgreSQL | 5432 | (Railway only) |

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 503 | Service Unavailable (Redis down) |

---

## Lead Processing States

| Status | Description |
|--------|-------------|
| pending | Lead created, waiting for processing |
| processing | Worker is processing lead |
| success | Successfully sent to GoHighLevel |
| failed | Failed after 3 retry attempts |

---

For detailed information, see:
- **[API Reference](API_REFERENCE.md)**
- **[Railway Deployment](RAILWAY_DEPLOYMENT.md)**
- **[Main README](../README.md)**
