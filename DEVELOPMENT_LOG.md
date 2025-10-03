# Development Log

## Technical Decisions & Architecture Notes

### Last Updated: 2025-10-03 08:46:15

---

## Technology Stack Decisions

### 1. Backend Framework: FastAPI ✅
**Decision Date**: 2025-10-03

**Rationale**:
- **Async Support**: Native async/await for handling concurrent AI requests
- **Performance**: Faster than Flask/Django for API-heavy applications
- **Auto Documentation**: Built-in Swagger UI and ReDoc
- **Type Safety**: Pydantic models for request/response validation
- **Modern Python**: Uses Python 3.11+ features
- **WebSocket Support**: Essential for real-time code execution feedback

**Alternatives Considered**:
- Django: Too heavyweight, more suited for traditional web apps
- Flask: Lacks native async support, requires more boilerplate

---

### 2. AI Provider: Google Gemini ✅
**Decision Date**: 2025-10-03

**Rationale**:
- **Cost-Effective**: Free tier available, affordable pricing
- **Quality**: Excellent for educational content generation
- **Multimodal**: Can handle text, code, and potentially images
- **API Simplicity**: Easy to integrate with Python SDK
- **Context Window**: Large enough for comprehensive lessons

**Alternatives Considered**:
- OpenAI GPT-4: More expensive, better for some tasks but overkill
- Claude: Excellent quality but API access limitations
- Open-source models: Lower quality for educational content

---

### 3. Topic Management: XML ✅
**Decision Date**: 2025-10-03

**Rationale**:
- **Human-Readable**: Easy for non-developers to edit
- **Hierarchical**: Natural fit for Course → Module → Lesson structure
- **Dynamic Updates**: No code changes needed to add topics
- **Validation**: Easy to validate structure with schemas
- **Lightweight**: No heavy database needed for topic metadata

**XML Structure**:
```xml
<course id="python-basics" language="python">
  <modules>
    <module id="oop">
      <lessons>
        <lesson id="classes" difficulty="beginner">
          <title>Classes and Objects</title>
          <keywords>class, object, methods</keywords>
        </lesson>
      </lessons>
    </module>
  </modules>
</course>
```

**Alternatives Considered**:
- JSON: Less readable for complex hierarchies
- YAML: Good but XML parsing more mature
- Database: Overkill for static topic metadata

---

### 4. Code Editor: Monaco Editor (Planned)
**Decision Date**: 2025-10-03

**Rationale**:
- **Battle-Tested**: Powers VS Code
- **Feature-Rich**: Syntax highlighting, autocomplete, IntelliSense
- **Multi-Language**: Supports all major languages
- **Customizable**: Easy to theme and configure
- **Performance**: Handles large files efficiently

**Alternative**: CodeMirror (lighter but less features)

---

### 5. Code Execution: Docker Sandbox ✅
**Decision Date**: 2025-10-03

**Rationale**:
- **Security**: Isolated containers prevent system access
- **Resource Limits**: CPU/memory constraints per execution
- **Multi-Language**: Easy to support Python, JS, Java, etc.
- **Consistency**: Same environment for all users
- **Scalability**: Can distribute across multiple containers

**Security Measures**:
- No network access inside containers
- Read-only filesystem (except /tmp)
- Execution timeout (30 seconds default)
- Memory limits (256MB default)
- No system calls allowed

---

## Project Structure Decisions

### Directory Organization
```
backend/
├── app/
│   ├── main.py              # FastAPI application entry
│   ├── api/routes/          # API endpoints
│   ├── core/                # Config, security, dependencies
│   ├── services/            # Business logic (AI, XML parser)
│   ├── models/              # Database models
│   └── schemas/             # Pydantic schemas
```

**Rationale**:
- **Separation of Concerns**: Clear boundaries between layers
- **Scalability**: Easy to add new modules
- **Testability**: Each component can be tested independently

---

## Database Schema (PostgreSQL)

### Tables Design

#### `users`
- Primary authentication and profile data
- Tracks user progress globally

#### `user_progress`
- Junction table: user_id + lesson_id
- Fields: completion_percentage, mastery_level, time_spent, last_accessed

#### `achievements`
- Gamification: badges, points, streaks
- Unlockable rewards

#### `quiz_attempts`
- Track quiz scores and history
- Used for adaptive difficulty

#### `generated_content` (Cache)
- Store AI-generated lessons temporarily
- Reduce API calls to Gemini
- TTL: 7 days

---

## API Design Patterns

### RESTful Endpoints

#### Lessons
- `GET /api/lessons` - List all available lessons
- `GET /api/lessons/{id}` - Get specific lesson (triggers AI generation if needed)
- `POST /api/lessons/{id}/complete` - Mark lesson as completed

#### Code Execution
- `POST /api/code/execute` - Execute user code in sandbox
- WebSocket `/ws/code` - Real-time code execution feedback

#### Practice
- `GET /api/practice/{lesson_id}/quiz` - Get/generate quiz
- `POST /api/practice/submit` - Submit quiz answers
- `GET /api/practice/{lesson_id}/game` - Get mini-game

#### User Progress
- `GET /api/progress` - Get user's overall progress
- `GET /api/progress/{course_id}` - Course-specific progress

---

## Performance Optimizations

### 1. Redis Caching Strategy
- **AI Responses**: Cache generated lessons (key: lesson_id)
- **User Sessions**: Fast session lookup
- **Leaderboards**: Real-time rankings without DB queries

### 2. Async Operations
- AI content generation runs async
- Code execution non-blocking
- Database queries use async SQLAlchemy

### 3. Response Streaming
- Stream AI-generated content as it's created
- Improves perceived performance

---

## Security Considerations

### 1. Code Execution Sandbox
- ✅ Docker containers with no internet
- ✅ Resource limits (CPU, memory, time)
- ✅ No file system access
- ✅ Whitelist allowed libraries

### 2. API Security
- JWT tokens for authentication
- Rate limiting on AI endpoints (prevent abuse)
- Input validation with Pydantic
- CORS configuration

### 3. Data Privacy
- No PII in logs
- Encrypt sensitive data at rest
- GDPR compliance for user data

---

## AI Content Generation Strategy

### Prompt Engineering
- **Structured Prompts**: JSON output format for parsing
- **Few-Shot Examples**: Include examples in prompts
- **Real-World Analogies**: Explicitly request relatable comparisons
- **Child-Friendly**: Target comprehension level for 10-12 year olds

### Content Caching
- Cache generated lessons for 7 days
- Version control for content updates
- Regenerate if topic keywords change

### Quality Control
- Fallback content if AI fails
- Manual review system (future)
- User feedback loop for improvements

---

## Gamification Design

### Progression System
1. **Mastery Levels**: 0-100% per topic
   - 0-30%: Novice
   - 31-60%: Apprentice
   - 61-85%: Competent
   - 86-95%: Proficient
   - 96-100%: Master

2. **Points System**:
   - Complete lesson: 10 points
   - Pass quiz (100%): 20 points
   - Complete mini-game: 15 points
   - Daily streak: +5 points/day

3. **Badges**:
   - "First Steps" - Complete first lesson
   - "Loop Master" - Master all loop topics
   - "OOP Wizard" - Master OOP module
   - "7-Day Streak" - Learn 7 days in a row

---

## Future Enhancements

### Phase 2 (Planned)
- [ ] Mobile app (React Native)
- [ ] Collaborative coding (real-time pair programming)
- [ ] Code review by AI
- [ ] Project-based learning tracks

### Phase 3 (Planned)
- [ ] Certification system
- [ ] Live instructor sessions
- [ ] Community forums
- [ ] Code competitions

---

## Known Limitations & Technical Debt

### Current Limitations
1. **No offline mode**: Requires internet for AI
2. **Limited languages**: Starting with Python only
3. **No mobile optimization**: Desktop-first design
4. **Single-user code execution**: No collaborative editing yet

### Technical Debt
- Need comprehensive test coverage
- API documentation needs examples
- Error handling improvements
- Logging standardization

---

## Dependencies & Versions

See [requirements.txt](backend/requirements.txt) for full list.

**Key Dependencies**:
- FastAPI 0.109.0
- Google Generative AI 0.3.2
- SQLAlchemy 2.0.25
- Redis 5.0.1
- Docker SDK 7.0.0

---

## Monitoring & Logging

### Logging Strategy (Loguru)
- **Structured Logs**: JSON format for parsing
- **Log Levels**:
  - DEBUG: Development only
  - INFO: Normal operations
  - WARNING: Recoverable issues
  - ERROR: Exceptions and failures
- **Rotation**: 500MB max per file, keep 10 days

### Metrics to Track
- AI request latency
- Code execution time
- Quiz completion rates
- User retention (daily/weekly active)

---

## Development Workflow

### Git Workflow
- Main branch: Production-ready
- Develop branch: Integration
- Feature branches: feature/feature-name

### Testing Strategy
- Unit tests: pytest
- Integration tests: API endpoint testing
- E2E tests: Selenium (future)

### CI/CD Pipeline (Future)
- GitHub Actions
- Auto-deploy to staging on PR merge
- Manual promotion to production

---

## Questions & Decisions Pending

1. **Authentication**: Social login (Google/GitHub) vs email/password?
2. **Deployment**: AWS vs GCP vs DigitalOcean?
3. **Payment Model**: Freemium vs subscription vs one-time?
4. **Content Moderation**: How to handle user-generated code examples?

---

**Note**: This log is updated with each major technical decision.
