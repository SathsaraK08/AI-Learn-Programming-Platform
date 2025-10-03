# 🚀 AI-Powered Programming Learning Platform

> **A revolutionary learning platform combining W3Schools' interactive coding + Replit's live environment + AI-powered personalized content generation**

## ⚡ Quick Start - One Command!

```bash
./start.sh
```

Then open: **http://localhost:8000**

That's it! Backend + Frontend in one command. See [START_HERE.md](START_HERE.md) for details.

---

## 🎯 Vision
Enable anyone (even children) to learn programming from zero to hero through:
- AI-generated content with real-world analogies
- Interactive code playground
- Gamified practice with memorable exercises
- Progress tracking and mastery levels

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Code Editor  │  │ Live Preview │  │ Quiz/Game UI    │   │
│  │ (Monaco)     │  │              │  │                 │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │ REST API / WebSocket
┌───────────────────────────▼─────────────────────────────────┐
│                    BACKEND LAYER (FastAPI)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ API Routes   │  │ WebSocket    │  │ Auth System     │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼─────────┐ ┌───────▼────────┐ ┌───────▼──────────┐
│  XML Topic      │ │ Gemini AI      │ │ Code Executor    │
│  Manager        │ │ Content Gen    │ │ (Docker Sandbox) │
│                 │ │                │ │                  │
│ - Parse topics  │ │ - Explanations │ │ - Python         │
│ - Dynamic load  │ │ - Examples     │ │ - JavaScript     │
│ - Version ctrl  │ │ - Analogies    │ │ - Java, etc.     │
└─────────────────┘ │ - Quizzes      │ └──────────────────┘
                    │ - Games        │
                    └────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼─────────┐ ┌───────▼────────┐ ┌───────▼──────────┐
│  PostgreSQL     │ │ Redis Cache    │ │ File Storage     │
│                 │ │                │ │                  │
│ - User data     │ │ - Sessions     │ │ - Generated      │
│ - Progress      │ │ - AI responses │ │   content        │
│ - Achievements  │ │ - Leaderboard  │ │ - User code      │
└─────────────────┘ └────────────────┘ └──────────────────┘
```

---

## 🧩 Core Components

### 1. **XML Topic Management System**
- Topics/courses defined in XML files
- Dynamic updates without code changes
- Hierarchical structure (Course → Module → Lesson)
- AI reads topic titles and generates content

**Example XML Structure:**
```xml
<course id="python-basics">
  <module id="oop">
    <lesson id="classes" difficulty="beginner">
      <title>Python Classes and Objects</title>
      <keywords>class, object, constructor, methods</keywords>
    </lesson>
  </module>
</course>
```

### 2. **AI Content Generator (Google Gemini)**
- Takes topic title from XML
- Generates:
  - Simple explanations
  - Real-world analogies
  - Code examples
  - Practice exercises
  - Quizzes
  - Mini-games for retention

### 3. **Interactive Code Playground**
- Split-pane editor (code + output)
- Multiple language support
- Real-time execution in sandboxed environment
- Syntax highlighting and autocomplete
- Code templates

### 4. **Gamified Practice System**
- Concept-specific mini-games
- Progressive difficulty
- Points and badges
- Mastery tracking (0-100%)
- Leaderboards

### 5. **Progress Tracking**
- User journey visualization
- Skill tree
- Time spent per topic
- Retention metrics

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **AI**: Google Gemini API
- **Database**: PostgreSQL (user data, progress)
- **Cache**: Redis (sessions, AI responses)
- **Code Execution**: Docker containers (isolated sandbox)

### Frontend
- **Editor**: Monaco Editor (VS Code's editor)
- **Framework**: React/Vue (or vanilla JS for simplicity)
- **Styling**: TailwindCSS
- **Real-time**: WebSocket

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **CI/CD**: GitHub Actions (future)

---

## 📁 Project Structure

```
LearnProgrm/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── lessons.py      # Lesson endpoints
│   │   │   │   ├── practice.py     # Quiz/game endpoints
│   │   │   │   ├── code_exec.py    # Code execution
│   │   │   │   └── users.py        # User management
│   │   ├── core/
│   │   │   ├── config.py           # Configuration
│   │   │   ├── security.py         # Auth logic
│   │   ├── services/
│   │   │   ├── ai_generator.py     # Gemini integration
│   │   │   ├── xml_parser.py       # XML topic parser
│   │   │   ├── code_runner.py      # Sandboxed execution
│   │   │   └── progress_tracker.py # User progress
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── lesson.py
│   │   │   └── progress.py
│   │   └── schemas/
│   │       └── lesson_schema.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   │   ├── editor.js
│   │   ├── api.js
│   │   └── game.js
│   └── assets/
├── data/
│   ├── topics/
│   │   ├── python.xml
│   │   ├── javascript.xml
│   │   └── java.xml
│   └── templates/
├── docker-compose.yml
├── .env.example
├── README.md
├── SESSION_LOG.md               # Development tracking
├── DEVELOPMENT_LOG.md           # Technical decisions log
└── ARCHITECTURE.md              # Detailed architecture
```

---

## 🚦 Getting Started

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Google Gemini API Key
- PostgreSQL (or use Docker)

### Installation

```bash
# Clone the repository
cd LearnProgrm

# Set up environment variables
cp .env.example .env
# Add your GEMINI_API_KEY to .env

# Build and run with Docker
docker-compose up --build

# Or run locally
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Environment Variables
```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql://user:password@localhost/learndb
REDIS_URL=redis://localhost:6379
SECRET_KEY=your_secret_key
```

---

## 🎮 Key Features

### 1. AI-Generated Content
- Topic title → AI researches → Generates comprehensive lesson
- Includes analogies (e.g., "Classes are like cookie cutters")
- Adaptive difficulty based on user level

### 2. Interactive Learning
- Write code in browser
- Instant feedback
- Step-by-step tutorials
- Hints system

### 3. Gamification
- **Mini-Games**: E.g., "OOP Escape Room" to practice classes
- **Badges**: "Loop Master", "Debugging Detective"
- **Challenges**: Daily coding challenges
- **Streak**: Keep learning daily

### 4. Smart Practice
- AI generates unique exercises
- Adaptive difficulty
- Spaced repetition for retention
- Code review with AI feedback

---

## 🗺️ Roadmap

### Phase 1: MVP (Current)
- [x] Project structure
- [ ] XML topic parser
- [ ] Gemini API integration
- [ ] Basic code editor
- [ ] Simple quiz system

### Phase 2: Interactive Learning
- [ ] Advanced code playground
- [ ] Multi-language support
- [ ] Code execution sandbox
- [ ] Progress tracking

### Phase 3: Gamification
- [ ] Mini-games for concepts
- [ ] Achievement system
- [ ] Leaderboards
- [ ] Social features

### Phase 4: Advanced Features
- [ ] AI code review
- [ ] Project-based learning
- [ ] Certification system
- [ ] Mobile app

---

## 📊 Current Status

**Last Updated**: 2025-10-03 08:42:53
**Phase**: 1 - MVP Development
**Progress**: 5%

See [SESSION_LOG.md](SESSION_LOG.md) for detailed development history.

---

## 👥 Contributing

This project uses detailed session logging for collaboration. Before starting work:
1. Read [SESSION_LOG.md](SESSION_LOG.md)
2. Create new session entry with timestamp
3. Document all changes
4. Update task completion status

---

## 📝 License

MIT License - See LICENSE file

---

## 🤝 Support

For questions or issues:
- Check [SESSION_LOG.md](SESSION_LOG.md) for recent changes
- Review [DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md) for technical decisions

---

**Built with ❤️ for making programming accessible to everyone**
# AI-powered-programming-learning-platform-
