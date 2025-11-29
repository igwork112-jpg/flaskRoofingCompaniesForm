# Roofing Lead Manager

A production-ready Flask application for managing and reactivating historical roofing leads through automated GoHighLevel CRM integration.

## Overview

This system enables roofing companies to upload historical customer leads and automatically sync them to GoHighLevel for SMS reactivation campaigns. The application handles lead validation, asynchronous processing, and comprehensive tracking.

## Key Features

- **Multi-Channel Lead Upload**: Web UI, CSV import, and REST API
- **Asynchronous Processing**: Redis-backed job queue for scalable lead processing
- **GoHighLevel Integration**: Automatic contact creation with retry logic
- **Company Management**: Multi-tenant support for multiple roofing companies
- **Processing Dashboard**: Real-time tracking of lead status and metrics
- **Production Ready**: Configured for Railway deployment with PostgreSQL

## Architecture

### Technology Stack

- **Backend**: Flask 3.0 (Python)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Queue**: Redis + RQ (Redis Queue)
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Flask-Migrate (Alembic)
- **Server**: Gunicorn (production)

### System Components

```
┌─────────────┐
│   Web UI    │
│   Forms     │
└──────┬──────┘
       │
┌──────▼──────┐     ┌─────────────┐
│   Flask     │────▶│  SQLite/    │
│   API       │     │  PostgreSQL │
└──────┬──────┘     └─────────────┘
       │
       │ Enqueue
       ▼
┌─────────────┐     ┌─────────────┐
│    Redis    │────▶│   Worker    │
│    Queue    │     │   Process   │
└─────────────┘     └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ GoHighLevel │
                    │     API     │
                    └─────────────┘
```

### Data Flow

1. **Lead Upload**: User submits leads via web form, CSV, or API
2. **Validation**: Server validates all fields (name, phone, company)
3. **Database Storage**: Valid leads saved to database
4. **Queue Job**: Lead processing job added to Redis queue
5. **Background Processing**: Worker picks up job and processes lead
6. **GHL Integration**: Worker sends lead to GoHighLevel API
7. **Status Tracking**: Processing log updated with success/failure status
8. **Retry Logic**: Failed jobs automatically retry up to 3 times

## Project Structure

```
flaskRoofingCompaniesForm-main/
├── app/
│   ├── api/                    # API endpoints
│   │   ├── bulk.py            # Bulk lead upload API
│   │   ├── company.py         # Company registration
│   │   ├── dashboard.py       # Dashboard endpoints
│   │   ├── health.py          # Health checks
│   │   ├── leads.py           # Single/CSV lead upload
│   │   └── web.py             # Web UI routes
│   ├── jobs/                   # Background jobs
│   │   └── process_lead.py    # Lead processing job
│   ├── models/                 # Database models
│   │   ├── company.py         # CompanyProfile model
│   │   ├── lead.py            # Lead model
│   │   └── log.py             # LeadProcessingLog model
│   ├── services/               # Business logic
│   │   ├── company_service.py # Company operations
│   │   ├── dashboard_service.py # Dashboard stats
│   │   ├── ghl_service.py     # GoHighLevel API client
│   │   ├── lead_service.py    # Lead operations
│   │   ├── logging_service.py # Log management
│   │   └── validation.py      # Input validation
│   ├── templates/              # HTML templates
│   ├── app.py                  # Flask app factory
│   ├── auth.py                 # Authentication (unused)
│   ├── extensions.py           # Flask extensions
│   └── queue.py                # Redis queue setup
├── tests/                      # Test suite (placeholder)
├── .env                        # Environment variables (local)
├── .gitignore                  # Git ignore rules
├── config.py                   # Configuration classes
├── Procfile                    # Railway/Heroku process file
├── railway.json                # Railway deployment config
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── run.py                      # Application entry point
├── runtime.txt                 # Python version
└── worker.py                   # Background worker startup
```

## Database Schema

### CompanyProfile
Stores roofing company information and GHL credentials.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| company_name | String(200) | Company name |
| owner_name | String(100) | Owner full name |
| owner_phone | String(20) | Owner phone |
| owner_email | String(100) | Owner email (unique) |
| ghl_location_id | String(100) | GoHighLevel location ID |
| created_at | DateTime | Registration timestamp |
| updated_at | DateTime | Last update timestamp |

### Lead
Stores customer lead information.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| company_id | Integer | Foreign key to CompanyProfile |
| name | String(100) | Lead full name |
| phone | String(20) | Lead phone number |
| notes | Text | Additional notes (optional) |
| created_at | DateTime | Upload timestamp |

### LeadProcessingLog
Tracks lead processing status and results.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| lead_id | Integer | Foreign key to Lead |
| company_id | Integer | Foreign key to CompanyProfile |
| status | String(20) | pending/processing/success/failed |
| worker_id | String(50) | Worker process ID |
| ghl_contact_id | String(100) | GHL contact ID (on success) |
| error_message | Text | Error details (on failure) |
| attempt_count | Integer | Number of retry attempts |
| created_at | DateTime | Log creation timestamp |
| updated_at | DateTime | Last status update |

## Documentation

- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Essential commands and endpoints
- **[API Reference](docs/API_REFERENCE.md)** - Complete API documentation with examples
- **[Railway Deployment](docs/RAILWAY_DEPLOYMENT.md)** - Production deployment guide

## Quick Start

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements-dev.txt
```

2. **Configure environment:**
Edit `.env` file and update `GHL_API_KEY` with your actual GoHighLevel API key.

3. **Start Redis:**
```bash
# Using Docker (recommended)
docker run -d -p 6379:6379 redis

# Or install Redis locally for your OS
```

4. **Start Flask app:**
```bash
python run.py
```

5. **Start worker (separate terminal):**
```bash
python worker.py
```

6. **Access application:**
```
http://localhost:5000
```

### Production Deployment

See **[Railway Deployment Guide](docs/RAILWAY_DEPLOYMENT.md)** for complete production setup with PostgreSQL and Redis.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| FLASK_ENV | Environment (development/production) | development |
| FLASK_SECRET_KEY | Flask secret key | dev-secret-key |
| DATABASE_URL | Database connection string | sqlite:///roofing_leads.db |
| REDIS_URL | Redis connection string | redis://localhost:6379/0 |
| GHL_API_KEY | GoHighLevel API key | (required) |
| GHL_API_BASE_URL | GoHighLevel API base URL | https://rest.gohighlevel.com/v1 |
| WORKER_COUNT | Number of worker processes | 4 |
| MAX_CSV_SIZE_MB | Maximum CSV file size | 10 |

## Lead Upload Methods

The application provides three methods for uploading leads:

1. **Web UI**: Browser-based forms for manual entry
2. **CSV Upload**: Bulk upload via CSV file (up to 10MB)
3. **REST API**: Programmatic bulk upload (requires Redis)

See **[API Reference](docs/API_REFERENCE.md)** for complete endpoint documentation and code examples.

## Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| GET | `/health` | System health check |
| GET | `/health/redis` | Redis status check |
| POST | `/company/register` | Register new company |
| POST | `/leads/single` | Upload single lead |
| POST | `/leads/csv` | Upload CSV file |
| POST | `/api/leads/bulk` | Bulk API upload |
| GET | `/dashboard` | Company dashboard |

## Background Processing

### Redis Queue

- **Queue Name**: `lead_processing`
- **Job Timeout**: 5 minutes
- **Result TTL**: 24 hours
- **Retry Policy**: 3 attempts with exponential backoff (1s, 2s, 4s)

### Worker Process

The worker process (`worker.py`) continuously polls the Redis queue and processes jobs:

1. Fetches lead and company from database
2. Creates processing log with "processing" status
3. Builds GoHighLevel contact payload
4. Attempts to create contact in GHL
5. Retries on failure (up to 3 times)
6. Updates log with final status (success/failed)

### Critical: Redis Requirement

**Bulk API uploads require Redis to be running.** If Redis is unavailable:
- Bulk API returns 503 error
- Single uploads work with fallback (for testing only)
- No leads are sent to GoHighLevel

Check Redis status: `GET /health/redis`

## Monitoring

### Health Checks

```bash
# Overall system health
curl http://localhost:5000/health

# Redis-specific health
curl http://localhost:5000/health/redis
```

### Processing Status

Monitor lead processing through the dashboard or query the database:

```sql
SELECT status, COUNT(*) 
FROM lead_processing_logs 
GROUP BY status;
```

## Security Considerations

### Current Implementation
- No authentication on bulk API endpoint
- Input validation on all fields
- SQL injection protection via SQLAlchemy ORM
- Environment variables for sensitive data

### Production Recommendations
- Add API key authentication
- Implement rate limiting
- Enable HTTPS only
- Add IP whitelisting
- Set up monitoring and alerting
- Regular security audits

## Development

### Adding New Features

1. **New API Endpoint**: Add to `app/api/`
2. **Business Logic**: Add to `app/services/`
3. **Database Model**: Add to `app/models/`
4. **Background Job**: Add to `app/jobs/`

### Database Migrations

```bash
# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

## Testing

Manual testing can be performed using the health check endpoints and API examples in the documentation.

```bash
# Check system health
curl http://localhost:5000/health

# Check Redis status
curl http://localhost:5000/health/redis
```

For API testing examples, see **[API Reference](docs/API_REFERENCE.md)**.

## Troubleshooting

### Common Issues

**App won't start:**
- Check Python version (3.11+ recommended)
- Verify all dependencies installed
- Check `.env` file exists

**Redis connection error:**
- Ensure Redis is running: `redis-cli ping`
- Check REDIS_URL in `.env`

**Database errors:**
- Run migrations: `flask db upgrade`
- Check DATABASE_URL format

**GHL API errors:**
- Verify GHL_API_KEY is correct
- Check ghl_location_id matches your account
- Review worker logs for details

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

Proprietary - All rights reserved

## Support

For issues and questions:
- Check documentation in `docs/` folder
- Review troubleshooting section
- Contact system administrator

---

**Version**: 1.0.0  
**Last Updated**: November 2024
