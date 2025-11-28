# ✅ All 3 Lead Upload Methods Are Ready!

## 🎉 You Now Have 3 Ways to Upload Leads

All methods use **the same field names** and store data in **the same database table**.

---

## Method 1: Single Lead Form 📝

**URL:** `http://localhost:5000/add-lead`

**Use Case:** Manual entry, one lead at a time

**How to Use:**
1. Open the URL in your browser
2. Select company from dropdown
3. Fill in: name, phone, notes
4. Click "Add Lead"

**Fields:**
- `name` - Lead name (required)
- `phone` - Lead phone (required)
- `notes` - Notes (optional)
- `company_id` - Select from dropdown

---

## Method 2: CSV Upload Form 📄

**URL:** `http://localhost:5000/upload-csv`

**Use Case:** Bulk upload via browser (hundreds or thousands of leads)

**How to Use:**
1. Open the URL in your browser
2. Select company from dropdown
3. Click "Choose CSV File"
4. Select your CSV file
5. Click "Upload CSV"

**CSV Format:**
```csv
name,phone,notes
John Smith,+1-555-1111,Interested in new roof
Mary Johnson,+1-555-2222,Repair needed
Bob Williams,+1-555-3333,Free inspection
```

**Download Sample CSV:**
Click the "Download Sample CSV" button on the page, or go to:
`http://localhost:5000/download-sample-csv`

---

## Method 3: Bulk API Endpoint 🔌

**URL:** `http://localhost:5000/api/leads/bulk`

**Use Case:** Automated integration from other systems

**Method:** POST with JSON

**Headers:**
- `Content-Type: application/json`
- `X-API-Key: your_api_key` (for now, any key works for testing)

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
    }
  ]
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:5000/api/leads/bulk ^
  -H "Content-Type: application/json" ^
  -H "X-API-Key: test_key" ^
  -d "{\"leads\":[{\"name\":\"John Smith\",\"phone\":\"+1-555-1111\",\"notes\":\"Test\",\"company_id\":1}]}"
```

---

## ✅ Consistent Field Names Across All Methods

| Field | Type | Required | Same in All 3 Methods |
|-------|------|----------|----------------------|
| `name` | string | Yes | ✅ |
| `phone` | string | Yes | ✅ |
| `notes` | string | No | ✅ |
| `company_id` | integer | Yes | ✅ |

---

## 🗄️ Database Storage

All 3 methods store data in the **same table** with **same columns**:

**Table:** `leads`

**Columns:**
- `id` - Auto-generated
- `company_id` - Foreign key to companies
- `name` - Lead name
- `phone` - Lead phone
- `notes` - Lead notes
- `created_at` - Timestamp

---

## 🧪 Test All 3 Methods

### Test Method 1 (Single Form):
1. Go to: `http://localhost:5000/add-lead`
2. Select a company
3. Enter: Name="Test Lead 1", Phone="+1-555-1111"
4. Submit

### Test Method 2 (CSV):
1. Create `test.csv`:
```csv
name,phone,notes
Test Lead 2,+1-555-2222,From CSV
Test Lead 3,+1-555-3333,From CSV
```
2. Go to: `http://localhost:5000/upload-csv`
3. Select company and upload file

### Test Method 3 (API):
```bash
curl -X POST http://localhost:5000/api/leads/bulk ^
  -H "Content-Type: application/json" ^
  -H "X-API-Key: test" ^
  -d "{\"leads\":[{\"name\":\"Test Lead 4\",\"phone\":\"+1-555-4444\",\"notes\":\"From API\",\"company_id\":1}]}"
```

---

## 📊 View Your Data

After uploading leads using any method, view them at:
- **Companies List:** `http://localhost:5000/companies`
- **Dashboard:** `http://localhost:5000/dashboard/1` (replace 1 with company ID)

---

## 🎯 Navigation Menu Updated

Your web interface now has:
- **Home** - Overview
- **Register Company** - Add companies
- **Add Lead** - Single lead form ← Method 1
- **Upload CSV** - CSV upload ← Method 2 (NEW!)
- **View Companies** - See all data

---

## 📖 Full Documentation

See `API_ENDPOINTS.md` for complete API documentation including:
- All endpoints
- Request/response examples
- Field validation rules
- Error handling
- Testing examples

---

## ✨ Summary

✅ **Method 1 (Single Form)** - Ready at `/add-lead`

✅ **Method 2 (CSV Upload)** - Ready at `/upload-csv`

✅ **Method 3 (Bulk API)** - Ready at `/api/leads/bulk`

✅ **All use same field names** - `name`, `phone`, `notes`, `company_id`

✅ **All store in same database** - `leads` table

✅ **All work without Redis/GHL** - Perfect for testing!

**Start testing now! Open http://localhost:5000 in your browser! 🚀**
