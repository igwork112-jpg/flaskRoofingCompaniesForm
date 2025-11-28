# 🧪 Testing Without Redis or GHL API

Perfect for initial testing! You can test the company registration and lead upload forms without Redis or GoHighLevel API.

## ✅ What Works Without Redis/GHL:

- ✅ Company registration
- ✅ Single lead upload
- ✅ CSV lead upload
- ✅ Dashboard viewing
- ✅ Database storage
- ✅ Form validation
- ⚠️ Background processing (skipped)
- ⚠️ GHL API integration (skipped)

## 🚀 Quick Start (2 Steps!)

### Step 1: Start the Flask App

```bash
python run.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 2: Test the Forms

**Option A - Use the Test Script:**
```bash
python test_forms.py
```

**Option B - Use curl:**

Register a company:
```bash
curl -X POST http://localhost:5000/company/register ^
  -H "Content-Type: application/json" ^
  -d "{\"company_name\":\"ABC Roofing\",\"owner_name\":\"John Doe\",\"owner_email\":\"john@abc.com\",\"owner_phone\":\"+1-555-1234\",\"ghl_location_id\":\"test123\"}"
```

Upload a lead:
```bash
curl -X POST http://localhost:5000/leads/single ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Jane Smith\",\"phone\":\"+1-555-5678\",\"notes\":\"Roof repair\",\"company_id\":1}"
```

View dashboard:
```bash
curl http://localhost:5000/dashboard/1
```

**Option C - Use Postman/Insomnia:**
1. Import the endpoints
2. Set Content-Type: application/json
3. Send requests!

## 📊 What You'll See

### Company Registration Response:
```json
{
  "message": "Company registered successfully",
  "company_id": 1,
  "company": {
    "id": 1,
    "company_name": "ABC Roofing",
    "owner_name": "John Doe",
    "owner_email": "john@abc.com",
    "owner_phone": "+1-555-1234",
    "ghl_location_id": "test123"
  }
}
```

### Lead Upload Response:
```json
{
  "message": "Lead uploaded successfully",
  "lead_id": 1,
  "job_id": "test-job-1",
  "lead": {
    "id": 1,
    "company_id": 1,
    "name": "Jane Smith",
    "phone": "+1-555-5678",
    "notes": "Roof repair"
  }
}
```

### Dashboard Response:
```json
{
  "company": {
    "id": 1,
    "company_name": "ABC Roofing",
    ...
  },
  "statistics": {
    "total_leads": 1,
    "counts_by_status": {
      "pending": 1,
      "processing": 0,
      "success": 0,
      "failed": 0
    },
    "success_rate": 0.0,
    "failed_leads": []
  }
}
```

## 🗄️ Database

All data is stored in `roofing_leads.db` (SQLite file).

You can view it with:
- DB Browser for SQLite: https://sqlitebrowser.org/
- Or any SQLite viewer

Tables created:
- `company_profiles` - Your registered companies
- `leads` - All uploaded leads
- `lead_processing_logs` - Processing status

## 🧪 Test CSV Upload

Create a test CSV file (`test_leads.csv`):
```csv
name,phone,notes
John Smith,+1-555-1111,New roof needed
Mary Johnson,+1-555-2222,Repair leak
Bob Williams,+1-555-3333,Inspection request
```

Upload it:
```bash
curl -X POST http://localhost:5000/leads/csv ^
  -F "file=@test_leads.csv" ^
  -F "company_id=1"
```

## ⚠️ What's Skipped (For Now)

**Without Redis:**
- Leads won't be queued for background processing
- They'll just get a fake job ID like "test-job-1"
- This is fine for testing forms and database

**Without GHL API:**
- Leads won't be sent to GoHighLevel
- No SMS campaigns will trigger
- This is fine for testing the upload flow

## 🔄 When You're Ready for Full Functionality

1. **Install Redis:**
   ```bash
   # WSL
   wsl
   sudo apt-get install redis-server
   redis-server
   ```

2. **Add GHL API Key to `.env`:**
   ```
   GHL_API_KEY=your_actual_api_key
   ```

3. **Start the worker:**
   ```bash
   python worker.py
   ```

Now leads will be processed in the background and sent to GHL!

## 🎯 Testing Checklist

- [ ] Health check works (`/health`)
- [ ] Can register a company
- [ ] Can upload a single lead
- [ ] Can upload CSV with multiple leads
- [ ] Can view dashboard
- [ ] Data persists in database
- [ ] Form validation works (try invalid data)

## 💡 Tips

**Test validation by trying invalid data:**
- Empty company name
- Invalid email format
- Invalid phone format
- Non-existent company_id for leads

**Check the database:**
```bash
# Install sqlite3 if needed
sqlite3 roofing_leads.db
.tables
SELECT * FROM company_profiles;
SELECT * FROM leads;
.quit
```

## 🆘 Troubleshooting

**"Connection refused"**
- Make sure Flask is running: `python run.py`
- Check it's on port 5000

**"Company with this email already exists"**
- Use a different email
- Or delete the database: `del roofing_leads.db` and restart

**"company_id does not exist"**
- Register a company first
- Use the company_id from the registration response

---

**You're all set for testing! 🎉**

Test the forms, validate the data flow, and when ready, add Redis + GHL for full functionality!
