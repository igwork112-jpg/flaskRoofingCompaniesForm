# 📡 API Endpoints Documentation

## All 3 Methods to Upload Leads

All methods use the **same column/field names** for consistency:
- `name` - Lead's full name
- `phone` - Lead's phone number
- `notes` - Additional notes (optional)
- `company_id` - The company this lead belongs to

---

## Method 1: Single Lead via Web Form

**URL:** `http://localhost:5000/add-lead`

**Method:** Web Form (GET to view, POST to submit)

**How to Use:**
1. Open in browser: `http://localhost:5000/add-lead`
2. Select company from dropdown
3. Fill in the form
4. Click "Add Lead"

**Form Fields:**
- `company_id` - Select from dropdown (required)
- `name` - Lead name (required)
- `phone` - Lead phone (required)
- `notes` - Additional notes (optional)

---

## Method 2: CSV Upload via Web Form

**URL:** `http://localhost:5000/upload-csv`

**Method:** Web Form with File Upload (GET to view, POST to submit)

**How to Use:**
1. Open in browser: `http://localhost:5000/upload-csv`
2. Select company from dropdown
3. Choose your CSV file
4. Click "Upload CSV"

**CSV Format:**
```csv
name,phone,notes
John Smith,+1-555-1111,Interested in new roof
Mary Johnson,+1-555-2222,Repair needed
Bob Williams,+1-555-3333,Free inspection
```

**Required CSV Columns:**
- `name` - Lead name (required)
- `phone` - Lead phone (required)
- `notes` - Additional notes (optional)

**Download Sample CSV:**
`http://localhost:5000/download-sample-csv`

---

## Method 3: Bulk API Endpoint (JSON)

**URL:** `http://localhost:5000/api/leads/bulk`

**Method:** POST

**Content-Type:** `application/json`

**Authentication:** Requires `X-API-Key` header (any value works for testing, e.g., "123")

**Request Body:**
```json
{
  "leads": [
    {
      "name": "John Smith",
      "phone": "+1-555-1111",
      "notes": "Interested in new roof",
      "company_id": 1
    },
    {
      "name": "Mary Johnson",
      "phone": "+1-555-2222",
      "notes": "Repair needed",
      "company_id": 1
    },
    {
      "name": "Bob Williams",
      "phone": "+1-555-3333",
      "notes": "Free inspection",
      "company_id": 1
    }
  ]
}
```

**Example using curl:**
```bash
curl -X POST http://localhost:5000/api/leads/bulk \
  -H "Content-Type: application/json" \
  -H "X-API-Key: 123" \
  -d '{
    "leads": [
      {
        "name": "John Smith",
        "phone": "+1-555-1111",
        "notes": "Interested in new roof",
        "company_id": 1
      }
    ]
  }'
```

**For Windows PowerShell:**
```powershell
curl -X POST http://localhost:5000/api/leads/bulk `
  -H "Content-Type: application/json" `
  -H "X-API-Key: 123" `
  -d '{\"leads\":[{\"name\":\"John Smith\",\"phone\":\"+1-555-1111\",\"notes\":\"Test\",\"company_id\":1}]}'
```

**Response:**
```json
{
  "message": "Bulk upload processed",
  "summary": {
    "total_submitted": 3,
    "valid": 3,
    "invalid": 0,
    "created": 3,
    "enqueued": 3,
    "failed": 0
  },
  "invalid_leads": [],
  "job_ids": ["test-job-1", "test-job-2", "test-job-3"]
}
```

---

## Field Names Summary

**All 3 methods use these exact same field names:**

| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| `name` | string | Yes | Lead's full name |
| `phone` | string | Yes | Lead's phone number (can include +, -, (), spaces) |
| `notes` | string | No | Additional notes about the lead |
| `company_id` | integer | Yes | ID of the company this lead belongs to |

---

## Additional API Endpoints

### Register Company
**URL:** `POST /company/register`

**Request Body:**
```json
{
  "company_name": "ABC Roofing",
  "owner_name": "John Doe",
  "owner_email": "john@abcroofing.com",
  "owner_phone": "+1-555-1234",
  "ghl_location_id": "test"
}
```

### Single Lead Upload (API)
**URL:** `POST /leads/single`

**Request Body:**
```json
{
  "name": "Jane Smith",
  "phone": "+1-555-5678",
  "notes": "Interested in roof repair",
  "company_id": 1
}
```

### CSV Upload (API)
**URL:** `POST /leads/csv`

**Method:** Multipart Form Data

**Form Fields:**
- `file` - CSV file
- `company_id` - Company ID

**Example using curl:**
```bash
curl -X POST http://localhost:5000/leads/csv \
  -F "file=@leads.csv" \
  -F "company_id=1"
```

### View Dashboard
**URL:** `GET /dashboard/{company_id}`

**Example:** `http://localhost:5000/dashboard/1`

### Health Check
**URL:** `GET /health`

**Example:** `http://localhost:5000/health`

---

## Database Schema

All leads are stored in the `leads` table with these columns:

```sql
CREATE TABLE leads (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Testing Examples

### Test Single Lead (Web Form)
1. Go to: `http://localhost:5000/add-lead`
2. Fill form and submit

### Test CSV Upload (Web Form)
1. Create `test.csv`:
```csv
name,phone,notes
John Smith,+1-555-1111,Test lead 1
Mary Johnson,+1-555-2222,Test lead 2
```
2. Go to: `http://localhost:5000/upload-csv`
3. Upload file

### Test Bulk API
```bash
curl -X POST http://localhost:5000/api/leads/bulk \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test_key" \
  -d '{
    "leads": [
      {"name": "Test Lead", "phone": "+1-555-9999", "notes": "API test", "company_id": 1}
    ]
  }'
```

---

## Important Notes

✅ **All 3 methods use identical field names** - `name`, `phone`, `notes`, `company_id`

✅ **All data goes to the same database table** - `leads`

✅ **Phone validation is consistent** - Accepts +, -, (), spaces, and digits

✅ **Name validation is consistent** - Cannot be empty or whitespace only

✅ **Company ID validation is consistent** - Must exist in `company_profiles` table

✅ **Works without Redis** - For testing, leads get fake job IDs

✅ **Works without GHL API** - For testing, just use "test" as location ID

---

## Quick Reference

| Method | URL | Use Case |
|--------|-----|----------|
| Web Form (Single) | `/add-lead` | Manual entry, one lead at a time |
| Web Form (CSV) | `/upload-csv` | Bulk upload via browser |
| API (Bulk) | `/api/leads/bulk` | Automated integration, multiple leads |

**All methods store data using the same field names and database structure!**
