# Quick Start Guide

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
copy .env.example .env
```

Edit `.env` and configure:
- `DATABASE_URL` - Your database connection (SQLite for dev: `sqlite:///roofing_leads.db`)
- `REDIS_URL` - Redis connection (default: `redis://localhost:6379/0`)
- `GHL_API_KEY` - Your GoHighLevel API key
- `FLASK_SECRET_KEY` - A random secret key

3. **Install and start Redis:**

**Windows:**
- Download Redis from https://github.com/microsoftarchive/redis/releases
- Or use WSL: `sudo apt-get install redis-server && redis-server`

**Mac:**
```bash
brew install redis
redis-server
```

**Linux:**
```bash
sudo apt-get install redis-server
redis-server
```

4. **Initialize the database:**
```bash
python run.py
```
(This will create tables automatically on first run)

5. **Start the Flask application:**
```bash
python run.py
```

6. **Start background workers (in a new terminal):**
```bash
python worker.py
```

## Testing the API

### 1. Register a Company
```bash
curl -X POST http://localhost:5000/company/register \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "ABC Roofing",
    "owner_name": "John Doe",
    "owner_email": "john@abcroofing.com",
    "owner_phone": "+1-555-1234",
    "ghl_location_id": "your_ghl_location_id"
  }'
```

### 2. Upload a Single Lead
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

### 3. View Dashboard
```bash
curl http://localhost:5000/dashboard/1
```

### 4. Health Check
```bash
curl http://localhost:5000/health
```

## Project Structure

```
roofing-lead-manager/
├── app/
│   ├── api/              # API endpoints
│   │   ├── company.py    # Company registration
│   │   ├── leads.py      # Lead upload (single & CSV)
│   │   ├── bulk.py       # Bulk API upload
│   │   ├── dashboard.py  # Dashboard endpoints
│   │   └── health.py     # Health checks
│   ├── models/           # Database models
│   │   ├── company.py    # CompanyProfile model
│   │   ├── lead.py       # Lead model
│   │   └── log.py        # LeadProcessingLog model
│   ├── services/         # Business logic
│   │   ├── validation.py       # Input validation
│   │   ├── company_service.py  # Company operations
│   │   ├── lead_service.py     # Lead operations
│   │   ├── logging_service.py  # Log operations
│   │   ├── ghl_service.py      # GHL API integration
│   │   └── dashboard_service.py # Dashboard stats
│   ├── jobs/             # Background jobs
│   │   └── process_lead.py     # Lead processing job
│   ├── app.py            # Flask app factory
│   ├── extensions.py     # Flask extensions
│   ├── queue.py          # Redis queue setup
│   └── auth.py           # API authentication
├── tests/                # Tests (to be implemented)
├── config.py             # Configuration
├── run.py                # Application entry point
├── worker.py             # Worker startup script
├── requirements.txt      # Python dependencies
└── .env.example          # Environment template
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/company/register` | Register a roofing company |
| POST | `/leads/single` | Upload a single lead |
| POST | `/leads/csv` | Upload leads via CSV file |
| POST | `/api/leads/bulk` | Bulk upload via API (requires API key) |
| GET | `/dashboard/<company_id>` | View company dashboard |
| GET | `/api/dashboard/<company_id>/stats` | Get dashboard stats as JSON |
| GET | `/health` | Health check |

## Next Steps

1. Configure your GoHighLevel API credentials in `.env`
2. Test the company registration endpoint
3. Upload some test leads
4. Monitor the worker logs to see leads being processed
5. Check the dashboard to see statistics

## Troubleshooting

**Redis connection error:**
- Make sure Redis is running: `redis-cli ping` should return `PONG`

**Database errors:**
- Check your `DATABASE_URL` in `.env`
- For SQLite, make sure the directory is writable

**GHL API errors:**
- Verify your `GHL_API_KEY` is correct
- Check that `ghl_location_id` matches your GHL sub-account

**Worker not processing jobs:**
- Make sure Redis is running
- Check that the worker is connected to the same Redis instance as the Flask app
- Look for errors in the worker terminal
