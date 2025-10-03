# 🚀 Quick Start Guide

## Get Started in 5 Minutes

### Prerequisites
- Python 3.11 or higher
- Google Gemini API Key ([Get one free](https://ai.google.dev/))

### Step 1: Set Up Environment

```bash
# Navigate to project
cd LearnProgrm

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### Step 3: Run the Backend

```bash
# From backend directory
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
🚀 Starting AI Learn Programming Platform
✅ All services initialized successfully
```

### Step 4: Open the Frontend

1. Open `frontend/index.html` in your browser
2. Or use a simple HTTP server:

```bash
# From project root
cd frontend
python -m http.server 3000
```

Then visit: `http://localhost:3000`

### Step 5: Start Learning!

1. Click on "Python Programming - Zero to Hero" in the sidebar
2. Select a module (e.g., "Python Fundamentals")
3. Click on any lesson (e.g., "Variables and Data Types")
4. Watch AI generate your personalized lesson!

---

## Testing the API

### Check API Health
```bash
curl http://localhost:8000/health
```

### Get Available Courses
```bash
curl http://localhost:8000/api/lessons/courses
```

### Get a Lesson (AI will generate content)
```bash
curl http://localhost:8000/api/lessons/variables
```

### Generate a Quiz
```bash
curl http://localhost:8000/api/lessons/variables/quiz
```

---

## Troubleshooting

### Backend won't start
- **Check Python version**: `python --version` (need 3.11+)
- **Check if port 8000 is in use**: `lsof -i :8000` (macOS/Linux)
- **Activate virtual environment**: `source venv/bin/activate`

### API returns 500 errors
- **Check Gemini API key**: Make sure it's valid in `.env`
- **Check logs**: Look at terminal output for error messages
- **Check XML files**: Make sure `data/topics/python.xml` exists

### Frontend can't connect to backend
- **Check backend is running**: Visit `http://localhost:8000/health`
- **Check CORS settings**: Make sure `ALLOWED_ORIGINS` includes your frontend URL
- **Check browser console**: Press F12 and look for errors

### AI content generation is slow
- **Normal behavior**: First request takes 5-10 seconds
- **Check internet**: Gemini API requires internet connection
- **Check API quota**: Free tier has rate limits

---

## Next Steps

Once everything is running:

1. **Explore the Python Course**: Navigate through all modules
2. **Try the Code Editor**: Switch to "Practice" tab and write code
3. **Take a Quiz**: Click "Quiz" tab after completing a lesson
4. **Play a Mini-Game**: Check out the "Mini-Game" tab

For development:
- Read [SESSION_LOG.md](SESSION_LOG.md) for what's been done
- Check [DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md) for technical details
- See [README.md](README.md) for full architecture

---

## Development Mode

### Enable Debug Logging
In `.env`, set:
```
DEBUG=True
LOG_LEVEL=DEBUG
```

### Auto-reload Frontend Changes
Use browser extension like "Live Server" or:
```bash
# Install
npm install -g live-server

# Run from frontend directory
cd frontend
live-server --port=3000
```

### API Documentation
Visit: `http://localhost:8000/api/docs` for interactive API docs (Swagger UI)

---

## What's Working Now

✅ Backend API with FastAPI
✅ XML topic parsing (Python course included)
✅ Google Gemini AI content generation
✅ Lesson content with explanations and analogies
✅ Quiz generation
✅ Mini-game generation
✅ Frontend UI with Monaco code editor
✅ Course navigation
✅ Responsive design

## What's Coming Next

🔄 User authentication
🔄 Progress tracking
🔄 Code execution in sandbox
🔄 Database integration
🔄 Redis caching
🔄 Achievement system

See [SESSION_LOG.md](SESSION_LOG.md) → "Next Session TODO" for full roadmap.

---

**Need Help?** Check the session logs or create an issue!
