# Roofing Lead Manager

A Flask application that enables roofing companies to upload historical leads to GoHighLevel for automated SMS reactivation campaigns.

## Features

- Company profile registration
- Multiple lead upload methods (single form, CSV, API)
- Asynchronous lead processing with Redis Queue
- GoHighLevel API integration
- Comprehensive logging and monitoring dashboard

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy environment configuration:
```bash
cp .env.example .env
```

3. Edit `.env` with your configuration (database, Redis, GHL API key)

4. Initialize database:
```bash
flask db upgrade
```

5. Start Redis server:
```bash
redis-server
```

6. Start the Flask application:
```bash
flask run
```

7. Start background workers (in separate terminal):
```bash
python worker.py
```

## API Endpoints

- `POST /company/register` - Register a roofing company
- `POST /leads/single` - Upload a single lead
- `POST /leads/csv` - Upload leads via CSV file
- `POST /api/leads/bulk` - Bulk upload via API (requires authentication)
- `GET /dashboard/<company_id>` - View company dashboard
- `GET /health` - Health check endpoint

## Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## Project Structure

```
.
├── app/
│   ├── models/          # Database models
│   ├── services/        # Business logic
│   ├── api/             # API routes
│   └── jobs/            # Background jobs
├── tests/
│   ├── unit/            # Unit tests
│   └── property/        # Property-based tests
├── config.py            # Configuration
├── requirements.txt     # Dependencies
└── worker.py           # Worker startup script
```
