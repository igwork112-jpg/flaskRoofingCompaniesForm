# 🚀 Roofing Lead Manager - Ready to Use!

## ✅ Setup Complete!

Your Flask application is fully built and ready to run. All dependencies are installed and the database is configured.

## 📋 What You Have

A complete lead management system with:
- ✅ Company registration API
- ✅ Single lead upload
- ✅ CSV bulk upload
- ✅ Authenticated bulk API
- ✅ Background job processing
- ✅ GoHighLevel integration
- ✅ Dashboard with statistics
- ✅ Health monitoring

## 🎯 Quick Start (3 Steps)

### Step 1: Configure GoHighLevel API Key

Edit `.env` file and add your GHL API key:
```
GHL_API_KEY=your_actual_ghl_api_key_here
```

### Step 2: Install & Start Redis

**Option A - Using WSL (Recommended for Windows):**
```bash
wsl
sudo apt-get update
sudo apt-get install redis-server
redis-server
```

**Option B - Download Redis for Windows:**
- Download from: https://github.com/microsoftarchive/redis/releases
- Extract and run `redis-server.exe`

**Option C - Use Docker:**
```bash
docker run -d -p 6379:6379 redis
```

### Step 3: Start the Application

**Terminal 1 - Start Flask App:**
```bash
python run.py
```

**Terminal 2 - Start Background Workers:**
```bash
python worker.py
```

## 🧪 Test the API

### 1. Health Check
```bash
curl http://localhost:5000/health
```

### 2. Register a Company
```bash
curl -X POST http://localhost:5000/company/register ^
  -H "Content-Type: application/json" ^
  -d "{\"company_name\": \"ABC Roofing\", \"owner_name\": \"John Doe\", \"owner_email\": \"john@abcroofing.com\", \"owner_phone\": \"+1-555-1234\", \"ghl_location_id\": \"your_ghl_location_id\"}"
```

### 3. Upload a Lead
```bash
curl -X POST http://localhost:5000/leads/single ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Jane Smith\", \"phone\": \"+1-555-5678\", \"notes\": \"Interested in roof repair\", \"company_id\": 1}"
```

### 4. View Dashboard
```bash
curl http://localhost:5000/dashboard/1
```

## 📁 Project Structure

```
roofing-lead-manager/
├── app/
│   ├── api/              # All API endpoints
│   ├── models/           # Database models
│   ├── services/         # Business logic
│   └── jobs/             # Background jobs
├── .env                  # Your configuration (EDIT THIS!)
├── run.py                # Start the Flask app
├── worker.py             # Start background workers
└── requirements.txt      # Dependencies (already installed)
```

## 🔧 Configuration

Your `.env` file is already set up with:
- ✅ SQLite database (no setup needed)
- ✅ Redis connection
- ⚠️ **YOU NEED TO ADD:** Your GHL API key

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check if app is running |
| POST | `/company/register` | Register a roofing company |
| POST | `/leads/single` | Upload one lead |
| POST | `/leads/csv` | Upload CSV file with leads |
| POST | `/api/leads/bulk` | Bulk API upload (needs API key) |
| GET | `/dashboard/<id>` | View company dashboard |

## 🎨 Using Postman or Similar Tools

1. Import the endpoints above
2. Set `Content-Type: application/json` header
3. For bulk API, add header: `X-API-Key: <your_api_key>`

## ❓ Troubleshooting

**"Redis connection error"**
- Make sure Redis is running: `redis-cli ping` should return `PONG`
- Check REDIS_URL in `.env`

**"GHL API error"**
- Verify your GHL_API_KEY in `.env`
- Check that ghl_location_id matches your GHL sub-account

**"Worker not processing jobs"**
- Make sure Redis is running
- Check that worker.py is running in a separate terminal
- Look for errors in the worker terminal output

## 📚 Next Steps

1. **Test with real data**: Register your company and upload some test leads
2. **Monitor the worker**: Watch the worker terminal to see leads being processed
3. **Check the dashboard**: View statistics at `/dashboard/<company_id>`
4. **Integrate with your frontend**: Use the API endpoints in your web app
5. **Deploy to production**: See QUICKSTART.md for deployment tips

## 🆘 Need Help?

- Check `QUICKSTART.md` for detailed documentation
- Review `README.md` for project overview
- Look at the code in `app/` directory - it's well-commented!

---

**You're all set! Start Redis, run the app, and begin uploading leads! 🎉**
