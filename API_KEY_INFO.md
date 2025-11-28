# 🔑 API Key Information

## ✅ API Key Fixed for Testing!

The bulk API endpoint now accepts **any API key** for testing purposes.

---

## How to Use the Bulk API

### Required Header:
```
X-API-Key: 123
```

**Any value works!** Examples:
- `X-API-Key: 123`
- `X-API-Key: test`
- `X-API-Key: my-api-key`
- `X-API-Key: anything`

---

## Test with curl (Windows)

```bash
curl -X POST http://localhost:5000/api/leads/bulk ^
  -H "Content-Type: application/json" ^
  -H "X-API-Key: 123" ^
  -d "{\"leads\":[{\"name\":\"Test Lead\",\"phone\":\"+1-555-9999\",\"notes\":\"API test\",\"company_id\":1}]}"
```

---

## Test with Postman

**1. Set Method:** POST

**2. Set URL:** `http://localhost:5000/api/leads/bulk`

**3. Add Headers:**
- `Content-Type: application/json`
- `X-API-Key: 123`

**4. Add Body (raw JSON):**
```json
{
  "leads": [
    {
      "name": "John Smith",
      "phone": "+1-555-1111",
      "notes": "Test lead",
      "company_id": 1
    }
  ]
}
```

**5. Click Send!**

---

## Test with Python Script

Run the test script I created:

```bash
python test_bulk_api.py
```

This will test the bulk API with 3 sample leads.

---

## Expected Response

**Success (200):**
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

**Error (401) - Missing API Key:**
```json
{
  "error": "API key is required"
}
```

**Error (400) - Invalid Data:**
```json
{
  "error": "Request must contain a \"leads\" array"
}
```

---

## Production API Key Setup

**For production, you would:**

1. Generate unique API keys per company
2. Store them in the database
3. Validate against stored keys
4. Add rate limiting
5. Add key expiration

**Current setup is perfect for testing!**

---

## Quick Reference

| What | Value |
|------|-------|
| Endpoint | `POST /api/leads/bulk` |
| Header | `X-API-Key: 123` (or any value) |
| Content-Type | `application/json` |
| Body | `{"leads": [...]}` |
| Test Script | `python test_bulk_api.py` |

---

## ✅ Summary

- **API Key:** Any value works (e.g., "123")
- **Header:** `X-API-Key: 123`
- **Endpoint:** `POST /api/leads/bulk`
- **Test:** Use curl, Postman, or `test_bulk_api.py`

**Your bulk API is ready to test! 🚀**
