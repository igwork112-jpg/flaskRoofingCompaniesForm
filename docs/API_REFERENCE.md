# API Reference

Complete API documentation for the Roofing Lead Manager system.

## Base URL

**Local Development:**
```
http://localhost:5000
```

**Production:**
```
https://your-app.railway.app
```

---

## Authentication

Currently, no authentication is required for any endpoints. For production deployment, consider implementing API key authentication.

---

## Health & Status Endpoints

### Check System Health

Get overall system health status.

**Endpoint:** `GET /health`

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "checks": {
    "database": "healthy",
    "redis": "healthy",
    "bulk_uploads": "enabled"
  }
}
```

**Response (Redis Down):** `200 OK`
```json
{
  "status": "healthy",
  "checks": {
    "database": "healthy",
    "redis": "unavailable",
    "bulk_uploads": "disabled"
  },
  "warnings": ["Bulk API uploads are disabled while Redis is unavailable"]
}
```

### Check Redis Status

Get detailed Redis and queue information.

**Endpoint:** `GET /health/redis`

**Response (Healthy):** `200 OK`
```json
{
  "redis": "healthy",
  "queue": "healthy",
  "queue_name": "lead_processing",
  "pending_jobs": 5,
  "bulk_uploads": "enabled"
}
```

**Response (Unavailable):** `503 Service Unavailable`
```json
{
  "redis": "unavailable",
  "message": "Redis is not running. Bulk uploads are disabled.",
  "bulk_uploads": "disabled"
}
```

---

## Company Management

### Register Company

Register a new roofing company profile.

**Endpoint:** `POST /company/register`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "company_name": "ABC Roofing",
  "owner_name": "John Doe",
  "owner_email": "john@abcroofing.com",
  "owner_phone": "+1-555-1234",
  "ghl_location_id": "abc123xyz"
}
```

**Field Validation:**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| company_name | string | Yes | Non-empty |
| owner_name | string | Yes | Non-empty |
| owner_email | string | Yes | Valid email format, unique |
| owner_phone | string | Yes | Valid phone format |
| ghl_location_id | string | Yes | Non-empty |

**Success Response:** `201 Created`
```json
{
  "message": "Company registered successfully",
  "company_id": 1,
  "company": {
    "id": 1,
    "company_name": "ABC Roofing",
    "owner_name": "John Doe",
    "owner_email": "john@abcroofing.com",
    "owner_phone": "+1-555-1234",
    "ghl_location_id": "abc123xyz",
    "created_at": "2024-11-29T10:30:00",
    "updated_at": "2024-11-29T10:30:00"
  }
}
```

**Error Response:** `400 Bad Request`
```json
{
  "errors": {
    "owner_email": ["A company with this email already exists"]
  }
}
```

**Example (cURL):**
```bash
curl -X POST http://localhost:5000/company/register \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "ABC Roofing",
    "owner_name": "John Doe",
    "owner_email": "john@abcroofing.com",
    "owner_phone": "+1-555-1234",
    "ghl_location_id": "abc123xyz"
  }'
```

---

## Lead Upload Endpoints

### Upload Single Lead

Upload a single lead via API.

**Endpoint:** `POST /leads/single`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Jane Smith",
  "phone": "+1-555-5678",
  "notes": "Interested in roof repair",
  "company_id": 1
}
```

**Field Validation:**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| name | string | Yes | Non-empty |
| phone | string | Yes | Valid phone format |
| notes | string | No | Any text |
| company_id | integer | Yes | Must exist |

**Success Response:** `201 Created`
```json
{
  "message": "Lead uploaded successfully",
  "lead_id": 42,
  "job_id": "abc123-def456-ghi789",
  "lead": {
    "id": 42,
    "company_id": 1,
    "name": "Jane Smith",
    "phone": "+1-555-5678",
    "notes": "Interested in roof repair",
    "created_at": "2024-11-29T10:35:00"
  }
}
```

**Error Response:** `400 Bad Request`
```json
{
  "errors": {
    "name": ["Name cannot be empty or contain only whitespace"],
    "phone": ["Phone must contain at least one digit"]
  }
}
```

**Example (cURL):**
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

### Upload CSV File

Upload multiple leads via CSV file.

**Endpoint:** `POST /leads/csv`

**Headers:**
```
Content-Type: multipart/form-data
```

**Form Data:**
- `file`: CSV file
- `company_id`: Company ID (integer)

**CSV Format:**
```csv
name,phone,notes
John Smith,+1-555-1111,Interested in new roof
Mary Johnson,+1-555-2222,Roof repair needed
Bob Williams,+1-555-3333,Request for inspection
```

**Required Columns:**
- `name` (required)
- `phone` (required)
- `notes` (optional)

**Success Response:** `200 OK`
```json
{
  "message": "CSV processed successfully",
  "summary": {
    "total_rows": 3,
    "valid_rows": 3,
    "invalid_rows": 0,
    "leads_created": 3,
    "leads_enqueued": 3,
    "leads_failed": 0
  },
  "invalid_rows": [],
  "job_ids": ["job-1", "job-2", "job-3"]
}
```

**Error Response (Invalid CSV):** `400 Bad Request`
```json
{
  "error": "Missing required columns: name, phone"
}
```

**Example (cURL):**
```bash
curl -X POST http://localhost:5000/leads/csv \
  -F "file=@leads.csv" \
  -F "company_id=1"
```

### Bulk Upload API

Upload multiple leads programmatically (requires Redis).

**Endpoint:** `POST /api/leads/bulk`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "leads": [
    {
      "name": "John Doe",
      "phone": "+1-555-1234",
      "notes": "Interested in roof repair",
      "company_id": 1
    },
    {
      "name": "Jane Smith",
      "phone": "+1-555-5678",
      "notes": "Needs inspection",
      "company_id": 1
    }
  ]
}
```

**Field Validation:**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| name | string | Yes | Non-empty |
| phone | string | Yes | Valid phone format |
| notes | string | No | Any text |
| company_id | integer | Yes | Must exist |

**Success Response:** `200 OK`
```json
{
  "message": "Bulk upload processed",
  "summary": {
    "total_submitted": 2,
    "valid": 2,
    "invalid": 0,
    "created": 2,
    "enqueued": 2,
    "failed": 0
  },
  "invalid_leads": [],
  "job_ids": [
    "abc123-def456-ghi789",
    "xyz789-uvw456-rst123"
  ]
}
```

**Partial Success Response:** `200 OK`
```json
{
  "message": "Bulk upload processed",
  "summary": {
    "total_submitted": 3,
    "valid": 2,
    "invalid": 1,
    "created": 2,
    "enqueued": 2,
    "failed": 0
  },
  "invalid_leads": [
    {
      "index": 1,
      "data": {
        "name": "",
        "phone": "+1-555-9999",
        "company_id": 1
      },
      "errors": {
        "name": ["Name cannot be empty or contain only whitespace"]
      }
    }
  ],
  "job_ids": ["job-1", "job-2"]
}
```

**Error Response (Redis Down):** `503 Service Unavailable`
```json
{
  "error": "Service unavailable: Queue system is not running",
  "message": "Bulk uploads require Redis to be running. Please contact system administrator.",
  "status": "redis_unavailable"
}
```

**Error Response (Invalid Request):** `400 Bad Request`
```json
{
  "error": "Request must contain a \"leads\" array"
}
```

**Example (cURL):**
```bash
curl -X POST http://localhost:5000/api/leads/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "leads": [
      {
        "name": "John Doe",
        "phone": "+1-555-1234",
        "notes": "Interested in roof repair",
        "company_id": 1
      }
    ]
  }'
```

**Example (Python):**
```python
import requests

url = "http://localhost:5000/api/leads/bulk"
payload = {
    "leads": [
        {
            "name": "John Doe",
            "phone": "+1-555-1234",
            "notes": "Interested in roof repair",
            "company_id": 1
        }
    ]
}

response = requests.post(url, json=payload)
print(response.json())
```

**Example (JavaScript):**
```javascript
const axios = require('axios');

const url = 'http://localhost:5000/api/leads/bulk';
const payload = {
  leads: [
    {
      name: 'John Doe',
      phone: '+1-555-1234',
      notes: 'Interested in roof repair',
      company_id: 1
    }
  ]
};

axios.post(url, payload)
  .then(response => console.log(response.data))
  .catch(error => console.error(error.response.data));
```

---

## Dashboard Endpoints

### View Company Dashboard

Get dashboard with company statistics (Web UI).

**Endpoint:** `GET /dashboard`

**Response:** HTML page with company list and metrics

### Get Company Stats (API)

Get company statistics as JSON.

**Endpoint:** `GET /api/dashboard/<company_id>/stats`

**Response:** `200 OK`
```json
{
  "company": {
    "id": 1,
    "company_name": "ABC Roofing",
    "owner_name": "John Doe"
  },
  "stats": {
    "total_leads": 150,
    "pending": 5,
    "processing": 2,
    "success": 140,
    "failed": 3,
    "success_rate": 97.9
  }
}
```

---

## Validation Rules

### Name Validation
- Must not be empty
- Must not be only whitespace
- Can contain any characters (including unicode)

**Valid:**
- "John Doe"
- "Mary-Jane Smith"
- "José García"
- "李明"

**Invalid:**
- "" (empty)
- "   " (whitespace only)
- null

### Phone Validation
- Must contain at least one digit
- Can include: digits, spaces, parentheses, hyphens, plus signs
- International formats supported

**Valid:**
- "+1-555-1234"
- "(555) 123-4567"
- "555.123.4567"
- "+44 20 7123 4567"
- "5551234567"

**Invalid:**
- "" (empty)
- "call me" (no digits)
- "N/A"

### Email Validation
- Must be valid email format
- Must be unique (for company registration)

**Valid:**
- "john@example.com"
- "user+tag@domain.co.uk"

**Invalid:**
- "notanemail"
- "@example.com"
- "user@"

### Company ID Validation
- Must be a valid integer
- Company must exist in database

---

## Error Codes

| Status Code | Meaning | Common Causes |
|-------------|---------|---------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid input, validation error |
| 401 | Unauthorized | Missing/invalid authentication (future) |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Redis not running (bulk API) |

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider:
- 100 requests per minute per IP
- 1000 leads per request maximum
- Exponential backoff on failures

---

## Best Practices

### Batch Sizes
- **Recommended:** 100-500 leads per bulk request
- **Maximum:** No hard limit, but consider timeouts
- **For 1000+ leads:** Split into multiple requests

### Error Handling
Always check the response status and handle errors:

```python
response = requests.post(url, json=payload)

if response.status_code == 503:
    print("Redis unavailable - try again later")
elif response.status_code == 200:
    data = response.json()
    if data['invalid_leads']:
        print(f"Warning: {len(data['invalid_leads'])} leads failed validation")
```

### Retry Logic
Implement exponential backoff for failed requests:

```python
import time

def upload_with_retry(leads, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json={"leads": leads}, timeout=30)
            if response.status_code == 503:
                time.sleep(2 ** attempt)  # 1s, 2s, 4s
                continue
            return response.json()
        except requests.exceptions.Timeout:
            time.sleep(2 ** attempt)
    raise Exception("Failed after all retries")
```

### Validation Before Upload
Validate data client-side before uploading:

```python
def validate_lead(lead):
    errors = []
    if not lead.get('name', '').strip():
        errors.append("Name is required")
    if not lead.get('phone') or not any(c.isdigit() for c in lead['phone']):
        errors.append("Valid phone is required")
    if not lead.get('company_id'):
        errors.append("Company ID is required")
    return errors
```

---

## Webhooks (Future)

Webhook support for lead processing events is planned for future releases:
- `lead.created` - When lead is created
- `lead.processing` - When processing starts
- `lead.success` - When successfully sent to GHL
- `lead.failed` - When processing fails

---

## Support

For API issues:
1. Check `/health` and `/health/redis` endpoints
2. Review validation rules
3. Check request format matches examples
4. Verify company_id exists
5. Ensure Redis is running (for bulk uploads)

---

**API Version:** 1.0  
**Last Updated:** November 2024
