# Learn Programming Platform - Project Structure

## Overview
An interactive programming learning platform combining W3Schools-style tutorials with Replit-like code execution, designed for children with gamified learning and AI explanations.

## Technology Stack
- **Backend**: FastAPI (Python)
- **Database**: SQLite (development) / PostgreSQL (production)
- **AI Integration**: Google Gemini API
- **Frontend**: React.js with TypeScript
- **Code Execution**: Docker containers for sandboxing
- **Content Format**: XML/JSON based curriculum

## Project Structure

```
learn-programming/
│
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI application entry point
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   ├── settings.py           # Configuration settings
│   │   │   └── database.py           # Database configuration
│   │   ├── models/                   # Database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── lesson.py
│   │   │   ├── progress.py
│   │   │   └── achievement.py
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── lesson.py
│   │   │   └── code_execution.py
│   │   ├── api/                      # API routes
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── lessons.py
│   │   │   │   ├── code_execution.py
│   │   │   │   ├── ai_explanations.py
│   │   │   │   └── progress.py
│   │   ├── services/                 # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── gemini_service.py     # Google Gemini integration
│   │   │   ├── code_executor.py      # Code execution service
│   │   │   ├── content_manager.py    # XML/JSON content management
│   │   │   └── progress_tracker.py   # User progress tracking
│   │   ├── utils/                    # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── security.py           # Authentication utilities
│   │   │   ├── validators.py         # Input validation
│   │   │   └── helpers.py            # General helpers
│   │   └── middleware/               # Custom middleware
│   │       ├── __init__.py
│   │       ├── cors.py
│   │       └── error_handling.py
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Docker configuration
│   └── .env.example                  # Environment variables template
│
├── frontend/                         # React Frontend
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/               # Reusable components
│   │   │   ├── common/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   └── Loading.tsx
│   │   │   ├── editor/
│   │   │   │   ├── CodeEditor.tsx    # Interactive code editor
│   │   │   │   ├── OutputPanel.tsx   # Code execution output
│   │   │   │   └── EditorToolbar.tsx
│   │   │   ├── lessons/
│   │   │   │   ├── LessonViewer.tsx  # Lesson content display
│   │   │   │   ├── LessonList.tsx    # Course navigation
│   │   │   │   └── ProgressBar.tsx   # Lesson progress
│   │   │   ├── games/
│   │   │   │   ├── CodePuzzle.tsx    # Programming puzzles
│   │   │   │   ├── DragDropCode.tsx  # Drag & drop coding
│   │   │   │   └── QuizGame.tsx      # Interactive quizzes
│   │   │   └── ai/
│   │   │       ├── AiExplainer.tsx   # AI explanation component
│   │   │       └── ChatBot.tsx       # AI assistance chat
│   │   ├── pages/                    # Page components
│   │   │   ├── Home.tsx
│   │   │   ├── Lessons.tsx
│   │   │   ├── Playground.tsx        # Code playground
│   │   │   ├── Games.tsx
│   │   │   ├── Profile.tsx
│   │   │   └── Progress.tsx
│   │   ├── hooks/                    # Custom React hooks
│   │   │   ├── useCodeExecution.ts
│   │   │   ├── useAiExplanation.ts
│   │   │   └── useProgress.ts
│   │   ├── services/                 # API services
│   │   │   ├── api.ts                # API client configuration
│   │   │   ├── lessonService.ts
│   │   │   ├── codeService.ts
│   │   │   └── aiService.ts
│   │   ├── styles/                   # CSS/SCSS files
│   │   │   ├── globals.css
│   │   │   ├── components/
│   │   │   └── themes/
│   │   ├── utils/                    # Frontend utilities
│   │   │   ├── constants.ts
│   │   │   ├── helpers.ts
│   │   │   └── validators.ts
│   │   ├── types/                    # TypeScript type definitions
│   │   │   ├── api.ts
│   │   │   ├── lesson.ts
│   │   │   └── user.ts
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.js            # Tailwind CSS configuration
│
├── content/                          # Learning Content
│   ├── courses/                      # Course definitions
│   │   ├── python-basics/
│   │   │   ├── course.json           # Course metadata
│   │   │   ├── lessons/
│   │   │   │   ├── 01-hello-world.xml
│   │   │   │   ├── 02-variables.xml
│   │   │   │   └── 03-loops.xml
│   │   │   └── exercises/
│   │   │       ├── hello-world-game.json
│   │   │       └── variable-puzzle.json
│   │   ├── javascript-basics/
│   │   └── scratch-programming/
│   ├── templates/                    # Content templates
│   │   ├── lesson-template.xml
│   │   ├── exercise-template.json
│   │   └── game-template.json
│   └── assets/                       # Media files
│       ├── images/
│       ├── videos/
│       └── audio/
│
├── docker/                           # Docker configurations
│   ├── code-executor/                # Sandboxed code execution
│   │   ├── python/
│   │   │   └── Dockerfile
│   │   ├── javascript/
│   │   │   └── Dockerfile
│   │   └── java/
│   │       └── Dockerfile
│   └── docker-compose.yml            # Multi-container setup
│
├── docs/                             # Documentation
│   ├── API.md                        # API documentation
│   ├── CONTENT_FORMAT.md             # XML/JSON content format guide
│   ├── DEPLOYMENT.md                 # Deployment instructions
│   └── DEVELOPMENT.md                # Development setup guide
│
├── tests/                            # Test files
│   ├── backend/
│   │   ├── test_api.py
│   │   ├── test_services.py
│   │   └── test_models.py
│   └── frontend/
│       ├── components/
│       └── services/
│
├── scripts/                          # Utility scripts
│   ├── setup.sh                      # Development setup
│   ├── deploy.sh                     # Deployment script
│   └── content-validator.py          # Content validation
│
├── .gitignore
├── README.md
├── LICENSE
└── docker-compose.yml
```

## Key Features by Directory

### Backend (`/backend/`)
- **FastAPI Application**: RESTful API with automatic documentation
- **Google Gemini Integration**: AI-powered explanations and assistance
- **Code Execution Service**: Secure sandboxed code running
- **Content Management**: XML/JSON curriculum handling
- **Progress Tracking**: User advancement and achievements

### Frontend (`/frontend/`)
- **Interactive Code Editor**: Monaco Editor integration
- **Child-Friendly UI**: Colorful, intuitive design
- **Gamified Learning**: Programming puzzles and challenges
- **Real-time Feedback**: Instant code execution results
- **AI Chat Assistant**: Help when students get stuck

### Content (`/content/`)
- **Structured Curriculum**: XML/JSON based lesson format
- **Multi-Language Support**: Python, JavaScript, Scratch
- **Progressive Difficulty**: From visual blocks to text coding
- **Interactive Exercises**: Hands-on coding challenges

### Docker (`/docker/`)
- **Secure Execution**: Isolated containers for running user code
- **Multi-Language Support**: Separate containers per language
- **Resource Limits**: CPU/Memory constraints for safety

## Content Format Examples

### Lesson XML Structure
```xml
<lesson id="hello-world" title="Your First Program">
  <objectives>
    <objective>Learn what programming is</objective>
    <objective>Write your first Python program</objective>
  </objectives>
  <content>
    <section type="explanation">
      <title>What is Programming?</title>
      <text>Programming is like giving instructions to a computer...</text>
      <image>programming-intro.png</image>
    </section>
    <section type="code-example">
      <title>Hello World</title>
      <code language="python">print("Hello, World!")</code>
      <explanation>This tells the computer to say hello!</explanation>
    </section>
    <section type="interactive">
      <title>Try It Yourself</title>
      <starter-code>print("Hello, ")</starter-code>
      <hint>Add your name in quotes!</hint>
    </section>
  </content>
  <assessment>
    <challenge>Make the computer say hello to you by name</challenge>
    <expected-output>Hello, [Student Name]!</expected-output>
  </assessment>
</lesson>
```

### Game JSON Structure
```json
{
  "id": "variable-puzzle",
  "title": "Variable Memory Game",
  "type": "drag-drop",
  "difficulty": "beginner",
  "instructions": "Match the variable names with their values",
  "game_data": {
    "variables": [
      {"name": "age", "value": "10", "type": "number"},
      {"name": "name", "value": "Alice", "type": "string"}
    ],
    "code_blocks": ["age = 10", "name = 'Alice'"],
    "correct_matches": [
      {"variable": "age", "block": "age = 10"},
      {"variable": "name", "block": "name = 'Alice'"}
    ]
  },
  "rewards": {
    "points": 50,
    "badge": "Variable Master"
  }
}
```

## Development Phases

### Phase 1: Core Platform
1. FastAPI backend setup
2. Basic code execution engine
3. Simple React frontend
4. Content management system

### Phase 2: AI Integration
1. Google Gemini API integration
2. AI explanation service
3. Interactive chat assistant
4. Smart hint system

### Phase 3: Gamification
1. Programming games
2. Achievement system
3. Progress tracking
4. Leaderboards

### Phase 4: Advanced Features
1. Multi-language support
2. Collaborative coding
3. Teacher dashboard
4. Parent progress reports

## Environment Variables

```env
# Database
DATABASE_URL=sqlite:///./app.db

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Docker
DOCKER_REGISTRY=your_registry
CONTAINER_TIMEOUT=30

# Frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GEMINI_API_KEY=your_frontend_gemini_key
```

## Next Steps
1. Set up the backend FastAPI application
2. Create the database models
3. Implement Google Gemini integration
4. Build the content management system
5. Create the React frontend
6. Implement the code execution engine
7. Add gamification features
8. Deploy and test

---

*This structure is designed to be modular, scalable, and maintainable. Feel free to modify based on your specific requirements.*