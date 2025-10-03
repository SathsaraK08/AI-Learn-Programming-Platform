# 🚀 Quick Start - One Command!

## Start Everything with One Command

```bash
./start.sh
```

That's it! The script will:
1. ✅ Activate virtual environment (or create one)
2. ✅ Install dependencies if needed
3. ✅ Start backend API
4. ✅ Serve frontend automatically

Then open your browser to: **http://localhost:8000**

---

## What You Get

- **Frontend**: http://localhost:8000/
- **API Docs**: http://localhost:8000/api/docs
- **API Health**: http://localhost:8000/api/health

---

## Alternative - Manual Start

If you prefer to run manually:

```bash
cd backend
source ../.venv/bin/activate  # or: source .venv/bin/activate
python -m uvicorn app.main:app --reload
```

Then visit: http://localhost:8000

---

## Features

✨ **AI-Powered Learning** - Gemini generates lessons on the fly
💻 **Interactive Coding** - Write and test code in browser
🎯 **Smart Quizzes** - AI creates custom quizzes
🎮 **Mini-Games** - Fun practice challenges
📊 **Progress Tracking** - Track your learning journey

---

## Troubleshooting

### Permission Denied
```bash
chmod +x start.sh
./start.sh
```

### Port Already in Use
Change port in `start.sh` (line with `--port 8000`)

### Dependencies Missing
```bash
cd backend
pip install -r requirements-minimal.txt
```

---

**Need help?** Check [SESSION_LOG.md](SESSION_LOG.md) for development history.
