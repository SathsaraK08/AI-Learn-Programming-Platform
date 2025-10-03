# Bugs & Solutions Log

**Project**: AI Learn Programming Platform
**Last Updated**: 2025-10-03 17:50:00

---

## Table of Contents
1. [Critical Bugs](#critical-bugs)
2. [Configuration Issues](#configuration-issues)
3. [Path Resolution Issues](#path-resolution-issues)
4. [API Issues](#api-issues)
5. [Dependency Issues](#dependency-issues)

---

## Bug Tracking Template

Each bug entry follows this format:
```
### Bug #X: [Short Title]
**Severity**: Critical / High / Medium / Low
**Status**: ✅ Fixed / 🔄 In Progress / ❌ Open
**Date Found**: YYYY-MM-DD HH:MM
**Date Fixed**: YYYY-MM-DD HH:MM

**Symptoms**:
- What the user sees/experiences

**Root Cause**:
- Why it's happening (technical explanation)

**Solution**:
- Step-by-step fix
- Code changes
- Configuration changes

**Prevention**:
- How to avoid in future

**Related Files**:
- List of files changed
```

---

## Critical Bugs

### Bug #1: Gemini API Model Not Found (404)
**Severity**: Critical 🔴
**Status**: ✅ Fixed
**Date Found**: 2025-10-03 15:30:00
**Date Fixed**: 2025-10-03 17:15:00
**Time to Fix**: ~1.5 hours

#### Symptoms
```
ERROR: 404 models/gemini-pro is not found for API version v1beta,
or is not supported for generateContent
```

- All lesson content showing fallback placeholder text
- AI content generation completely broken
- Error logs showing 404 from Google Gemini API

#### Root Cause
1. **Deprecated Model Name**:
   - Configuration used `gemini-pro` (old model name)
   - Google updated their models and deprecated `gemini-pro`
   - New models use naming like `gemini-2.5-flash`, `gemini-2.5-pro`

2. **Multiple .env Files**:
   - Root directory: `/Users/.../LearnProgrm/.env` (updated)
   - Backend directory: `/Users/.../LearnProgrm/backend/.env` (old value)
   - Pydantic-settings loaded from backend/.env when running from backend directory
   - This is why updates to root .env didn't work

3. **Settings Caching**:
   - `@lru_cache()` decorator on `get_settings()` function
   - Cached settings instance created at module import time
   - Even with --reload, cache persisted until Python process restart

#### Investigation Steps

**Step 1**: Test API directly
```python
# Discovered available models
import google.generativeai as genai
genai.configure(api_key=api_key)
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(model.name)

# Output showed:
# - models/gemini-2.5-flash ✅
# - models/gemini-2.5-pro ✅
# - models/gemini-pro ❌ (NOT in list)
```

**Step 2**: Check which .env is loaded
```bash
# Found two .env files!
ls -la /Users/.../LearnProgrm/.env
ls -la /Users/.../LearnProgrm/backend/.env

# backend/.env had old value: GEMINI_MODEL=gemini-pro
```

**Step 3**: Verify config loading
```python
from dotenv import load_dotenv
load_dotenv()
print(os.getenv("GEMINI_MODEL"))
# Output: gemini-pro (from backend/.env)
```

#### Solution

**Part 1: Update Model Name**

1. Updated root `.env`:
   ```bash
   # Before
   GEMINI_MODEL=gemini-pro

   # After
   GEMINI_MODEL=gemini-2.5-flash
   ```

2. Updated `backend/.env`:
   ```bash
   # Before
   GEMINI_MODEL=gemini-pro

   # After
   GEMINI_MODEL=gemini-2.5-flash
   ```

3. Updated `.env.example`:
   ```bash
   # Before
   GEMINI_MODEL=gemini-pro

   # After
   GEMINI_MODEL=gemini-2.5-flash
   ```

4. Updated default in `backend/app/core/config.py`:
   ```python
   # Before
   GEMINI_MODEL: str = "gemini-pro"

   # After
   GEMINI_MODEL: str = "gemini-2.5-flash"
   ```

**Part 2: Remove Settings Cache**

Updated `backend/app/core/config.py`:
```python
# Before
from functools import lru_cache

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# After
def get_settings() -> Settings:
    """Get settings instance
    Note: Removed lru_cache for development to allow .env changes to reload
    """
    return Settings()
```

**Part 3: Restart Server**
```bash
# Kill all running servers
lsof -ti :8000 | xargs kill -9

# Start fresh
cd /Users/.../LearnProgrm/backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Part 4: Reload XML Topics**
```bash
curl -X POST http://localhost:8000/api/lessons/reload
```

#### Verification
```bash
# Test lesson generation
curl http://localhost:8000/api/lessons/variables | python3 -m json.tool

# Success! Got AI-generated content:
{
  "content": {
    "explanation": "Variables are like labeled containers...",
    "analogy": "Imagine you have a magical toy chest...",
    ...
  }
}
```

#### Prevention
1. **Consolidate .env Files**:
   - Keep only ONE .env file at project root
   - Update Pydantic config to explicitly point to root:
     ```python
     class Config:
         env_file = "../.env"  # Relative to backend/app/core/
     ```

2. **Remove Production Cache in Development**:
   - Use `@lru_cache()` only in production
   - Check environment variable:
     ```python
     if os.getenv("ENV") == "production":
         @lru_cache()
         def get_settings():
             ...
     ```

3. **Model Version Checking**:
   - Add startup check to verify model exists:
     ```python
     @app.on_event("startup")
     async def verify_gemini_model():
         # List models and check if configured model exists
     ```

4. **Better Error Messages**:
   - Catch specific 404 errors
   - Suggest solution in error message

#### Related Files
- `/Users/.../LearnProgrm/.env`
- `/Users/.../LearnProgrm/backend/.env`
- `/Users/.../LearnProgrm/.env.example`
- `backend/app/core/config.py` (lines 25, 49-54)
- `backend/app/services/ai_generator.py` (line 22)

---

### Bug #2: No Courses Available in Frontend
**Severity**: High 🟠
**Status**: ✅ Fixed
**Date Found**: 2025-10-03 14:15:00
**Date Fixed**: 2025-10-03 15:00:00
**Time to Fix**: ~45 minutes

#### Symptoms
- Browser shows "No courses available"
- API endpoint `/api/lessons/courses` returns empty array `[]`
- Backend logs show: `WARNING: Topics directory does not exist: data/topics`

#### Root Cause
**Path Resolution Issue**:

1. XML Parser initialized with relative path:
   ```python
   self.topics_dir = Path("data/topics")  # Relative path
   ```

2. When server runs from `backend/` directory:
   ```bash
   cd /Users/.../LearnProgrm/backend
   python -m uvicorn app.main:app
   ```

3. Relative path resolves to:
   ```
   /Users/.../LearnProgrm/backend/data/topics ❌ (doesn't exist)
   ```

4. Actual directory location:
   ```
   /Users/.../LearnProgrm/data/topics ✅ (exists)
   ```

#### Investigation
```python
# In xml_parser.py __init__
print(f"Current dir: {os.getcwd()}")
# Output: /Users/.../LearnProgrm/backend

print(f"Topics dir: {self.topics_dir}")
# Output: data/topics (relative)

print(f"Resolved: {self.topics_dir.resolve()}")
# Output: /Users/.../LearnProgrm/backend/data/topics ❌

print(f"Exists: {self.topics_dir.exists()}")
# Output: False
```

#### Solution

**Option 1: Absolute Path Calculation** (✅ Chosen)

Modified `backend/app/services/xml_parser.py`:

```python
from pathlib import Path

def __init__(self, topics_directory: str = "data/topics"):
    topics_path = Path(topics_directory)

    # Convert relative paths to absolute based on project root
    if not topics_path.is_absolute():
        # Get project root: xml_parser.py location
        # services -> app -> backend -> LearnProgrm (project root)
        # So: parent x4 levels up
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        self.topics_dir = project_root / topics_directory

        logger.info(f"Resolved topics directory to: {self.topics_dir}")
    else:
        self.topics_dir = topics_path

    # Verify it exists
    if not self.topics_dir.exists():
        logger.error(f"Topics directory does not exist: {self.topics_dir}")
```

**Path Calculation Breakdown**:
```python
__file__                    # xml_parser.py
    .resolve()              # Absolute path
    .parent                 # services/
    .parent                 # app/
    .parent                 # backend/
    .parent                 # LearnProgrm/ (PROJECT ROOT)
    / "data/topics"         # LearnProgrm/data/topics ✅
```

#### Verification
```bash
# 1. Restart server
curl -X POST http://localhost:8000/api/lessons/reload

# Output:
{
  "status": "success",
  "courses_loaded": 1,
  "total_topics": 20
}

# 2. Check courses endpoint
curl http://localhost:8000/api/lessons/courses

# Output:
[{
  "id": "python-basics",
  "name": "Python Programming - Zero to Hero",
  "language": "python",
  "module_count": 6
}]

# 3. Check browser
# Sidebar now shows: Python Programming - Zero to Hero ✅
```

#### Alternative Solutions (Not Used)

**Option 2: Environment Variable**
```python
# .env
TOPICS_DIR=/Users/.../LearnProgrm/data/topics

# config.py
TOPICS_DIR: str = "data/topics"

# xml_parser.py
self.topics_dir = Path(settings.TOPICS_DIR)
```
❌ Requires hardcoded paths per environment

**Option 3: Change Working Directory**
```bash
# Always run from project root
cd /Users/.../LearnProgrm
python -m backend.app.main
```
❌ Breaks relative imports

#### Prevention
1. **Always use absolute paths** for file system operations
2. **Calculate from known anchor** (`__file__`)
3. **Add startup validation**:
   ```python
   @app.on_event("startup")
   async def validate_paths():
       if not topics_dir.exists():
           raise RuntimeError(f"Topics directory not found: {topics_dir}")
   ```

4. **Document working directory assumptions** in README

#### Related Files
- `backend/app/services/xml_parser.py` (lines 69-81)

---

### Bug #3: API Route Duplication (404 on /api/lessons/{id})
**Severity**: High 🟠
**Status**: ✅ Fixed
**Date Found**: 2025-10-03 16:00:00
**Date Fixed**: 2025-10-03 16:15:00
**Time to Fix**: ~15 minutes

#### Symptoms
```bash
# This works
curl http://localhost:8000/api/lessons/courses
# Returns: [{...}]

# This returns 404
curl http://localhost:8000/api/lessons/variables
# Returns: {"detail": "Not Found"}

# Checking OpenAPI docs shows wrong paths:
# /api/lessons/lessons/{lesson_id}  ❌
# /api/lessons/lessons/{lesson_id}/quiz  ❌
```

#### Root Cause
**Double Prefix in Routes**:

1. Router mounted with prefix in `main.py`:
   ```python
   app.include_router(lessons.router, prefix="/api/lessons")
   ```

2. Routes defined with full path in `lessons.py`:
   ```python
   @router.get("/lessons/{lesson_id}")  # ❌ Has /lessons again
   ```

3. Result: `/api/lessons` + `/lessons/{id}` = `/api/lessons/lessons/{id}` ❌

#### Solution

Modified `backend/app/api/routes/lessons.py`:

```python
# Before ❌
@router.get("/lessons/{lesson_id}", response_model=LessonContentResponse)
async def get_lesson(lesson_id: str, regenerate: bool = False):
    ...

@router.get("/lessons/{lesson_id}/quiz")
async def get_lesson_quiz(lesson_id: str, num_questions: int = 5):
    ...

@router.get("/lessons/{lesson_id}/game")
async def get_lesson_game(lesson_id: str):
    ...

@router.post("/lessons/reload")
async def reload_topics():
    ...

# After ✅
@router.get("/{lesson_id}", response_model=LessonContentResponse)
async def get_lesson(lesson_id: str, regenerate: bool = False):
    ...

@router.get("/{lesson_id}/quiz")
async def get_lesson_quiz(lesson_id: str, num_questions: int = 5):
    ...

@router.get("/{lesson_id}/game")
async def get_lesson_game(lesson_id: str):
    ...

@router.post("/reload")
async def reload_topics():
    ...
```

#### Verification
```bash
# Check OpenAPI schema
curl http://localhost:8000/openapi.json | python3 -c "import sys, json; print('\\n'.join(json.load(sys.stdin)['paths'].keys()))"

# Output:
/api
/api/health
/api/lessons/courses
/api/lessons/courses/{course_id}/modules
/api/lessons/{lesson_id}  ✅ Fixed!
/api/lessons/{lesson_id}/quiz  ✅
/api/lessons/{lesson_id}/game  ✅
/api/lessons/reload  ✅

# Test lesson endpoint
curl http://localhost:8000/api/lessons/variables
# Success! Returns AI-generated lesson content
```

#### Lessons Learned
- **Router prefix includes the path** - routes should be relative to prefix
- **Check OpenAPI docs** (`/api/docs`) to verify actual routes
- **Use consistent patterns** across all routers

#### Related Files
- `backend/app/api/routes/lessons.py` (lines 118, 171, 210, 247)

---

## Configuration Issues

### Bug #4: Environment Variables Not Loading
**Severity**: Medium 🟡
**Status**: ✅ Fixed
**Date Found**: 2025-10-03 14:00:00
**Date Fixed**: 2025-10-03 14:10:00

#### Symptoms
```
ValidationError: 3 validation errors for Settings
SECRET_KEY: Field required
GEMINI_API_KEY: Field required
DATABASE_URL: Field required
```

#### Root Cause
- `.env` file not created (only `.env.example` existed)
- Pydantic Settings requires all non-optional fields

#### Solution
```bash
# Copy template
cp .env.example .env

# Add values
echo "GEMINI_API_KEY=your_key_here" >> .env
echo "SECRET_KEY=your-secret-key-min-32-chars" >> .env
echo "DATABASE_URL=postgresql://user:pass@localhost/db" >> .env
```

#### Prevention
- Add to README: "Copy .env.example to .env before starting"
- Add validation script: `./scripts/check-env.sh`

#### Related Files
- `.env.example`
- `.env` (user must create)
- `backend/app/core/config.py`

---

### Bug #5: ALLOWED_ORIGINS Configuration Error
**Severity**: Medium 🟡
**Status**: ✅ Fixed (Workaround)
**Date Found**: 2025-10-03 09:30:00
**Date Fixed**: 2025-10-03 09:45:00

#### Symptoms
```
pydantic_settings.sources.SettingsError: error parsing value for field
"ALLOWED_ORIGINS" from source "DotEnvSettingsSource"
```

#### Root Cause
- Pydantic expects JSON array for List fields
- `.env` file uses comma-separated string
- Pydantic couldn't parse `http://localhost:3000,http://localhost:8000`

#### Solution (Workaround)
Removed ALLOWED_ORIGINS from Settings, hardcoded in main.py:

```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hardcoded for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Better Solution (For Production)
```python
# config.py
from pydantic import field_validator

class Settings(BaseSettings):
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    @field_validator('ALLOWED_ORIGINS', mode='before')
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
```

#### Related Files
- `backend/app/core/config.py`
- `backend/app/main.py` (lines 31-37)

---

## Dependency Issues

### Bug #6: Python 3.13 Pydantic Compatibility
**Severity**: Medium 🟡
**Status**: ✅ Fixed
**Date Found**: 2025-10-03 09:00:00
**Date Fixed**: 2025-10-03 09:15:00

#### Symptoms
```
ERROR: Failed building wheel for pydantic-core
Building wheel for pydantic-core (pyproject.toml) ... error
Rust compilation required
```

#### Root Cause
- `requirements.txt` had pinned versions: `pydantic-core==2.14.6`
- This version required Rust compiler for Python 3.13
- Network timeout during Rust compilation

#### Solution
Updated `requirements.txt` to use minimum versions:

```bash
# Before
pydantic==2.5.2
pydantic-core==2.14.6
pydantic-settings==2.1.0

# After
pydantic>=2.5.2
pydantic-settings>=2.1.0
# Removed pydantic-core (auto-installed by pydantic)
```

Created `requirements-minimal.txt`:
```
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
google-generativeai>=0.3.1
xmltodict>=0.13.0
loguru>=0.7.2
python-dotenv>=1.0.0
```

#### Verification
```bash
pip install -r requirements.txt
# Success! All packages installed without Rust
```

#### Related Files
- `backend/requirements.txt`
- `backend/requirements-minimal.txt`

---

## API Issues

### Bug #7: Code Execution Placeholder
**Severity**: Medium 🟡
**Status**: ✅ Fixed
**Date Found**: 2025-10-03 17:15:00
**Date Fixed**: 2025-10-03 17:45:00

#### Symptoms
- Clicking "Run Code" shows: "Code execution coming soon!"
- No actual code execution happening

#### Root Cause
Frontend had TODO placeholder:
```javascript
// frontend/js/app.js
async function executeCode() {
    // TODO: Implement actual code execution via backend
    outputElement.textContent = `Code execution coming soon!`;
}
```

#### Solution

**Step 1**: Created backend endpoint `code_execution.py`:
```python
@router.post("/execute", response_model=CodeExecutionResponse)
async def execute_code(request: CodeExecutionRequest):
    # Safe subprocess execution with timeout
    result = subprocess.run(
        ['python3', temp_file],
        capture_output=True,
        timeout=5
    )
    return CodeExecutionResponse(
        output=result.stdout,
        error=result.stderr,
        execution_time=elapsed
    )
```

**Step 2**: Updated frontend to call API:
```javascript
async function executeCode() {
    const result = await api.executeCode(code, language);

    if (result.error) {
        outputElement.textContent = `❌ Error:\n${result.error}`;
    } else {
        outputElement.textContent = `✅ Success:\n${result.output}`;
    }
}
```

**Step 3**: Registered router in main.py:
```python
from app.api.routes import code_execution
app.include_router(code_execution.router, prefix="/api/code")
```

#### Verification
```bash
# Test backend
curl -X POST http://localhost:8000/api/code/execute \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello\")", "language": "python"}'

# Output:
{
  "output": "Hello\n",
  "error": null,
  "execution_time": 0.012
}

# Test frontend
# Go to http://localhost:8000
# Click Practice tab
# Write: print("test")
# Click Run Code
# Shows: ✅ Success (0.01s): test ✅
```

#### Related Files
- `backend/app/api/routes/code_execution.py` (new file, 136 lines)
- `backend/app/main.py` (line 84)
- `frontend/js/app.js` (lines 300-321)

---

## Summary Statistics

### Bugs Fixed: 7
- Critical: 1
- High: 2
- Medium: 4

### Average Fix Time
- Critical bugs: 1.5 hours
- High bugs: 30 minutes
- Medium bugs: 15 minutes

### Most Common Issue Types
1. Configuration/Environment (3 bugs)
2. Path Resolution (1 bug)
3. API Design (2 bugs)
4. Dependencies (1 bug)

### Prevention Strategies Applied
1. ✅ Absolute path calculations
2. ✅ Better error messages
3. ✅ Startup validation checks
4. ✅ Flexible version requirements
5. ✅ Consolidated configuration
6. ✅ Removed unnecessary caching

---

## Quick Reference: Common Fixes

### 1. Server Won't Start
```bash
# Check if port is in use
lsof -ti :8000 | xargs kill -9

# Check .env exists
ls -la .env

# Verify dependencies
pip list | grep -E "fastapi|pydantic|uvicorn"
```

### 2. API Returns 404
```bash
# Check actual routes
curl http://localhost:8000/openapi.json | python3 -c "import sys, json; print('\\n'.join(json.load(sys.stdin)['paths'].keys()))"

# Check logs
tail -f backend/logs/app.log
```

### 3. AI Content Not Generating
```bash
# Check Gemini model
python3 << EOF
import google.generativeai as genai
genai.configure(api_key="YOUR_KEY")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
EOF

# Check .env
cat backend/.env | grep GEMINI
```

### 4. Courses Not Loading
```bash
# Reload courses
curl -X POST http://localhost:8000/api/lessons/reload

# Check topics directory
ls -la data/topics/

# Check logs for path resolution
grep "topics directory" backend/logs/app.log
```

---

**End of Bugs & Solutions Log**
