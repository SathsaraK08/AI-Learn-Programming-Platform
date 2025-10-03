// Main application logic

let currentLesson = null;
let currentCourse = null;

// Initialize application
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Initializing AI Learn Programming Platform');

    // Initialize Monaco Editor
    initializeMonacoEditor();

    // Load courses
    await loadCourses();

    // Set up event listeners
    setupEventListeners();

    console.log('✅ Application initialized');
});

// Load all courses
async function loadCourses() {
    try {
        const courses = await api.getCourses();
        displayCourses(courses);
    } catch (error) {
        console.error('Failed to load courses:', error);
        document.getElementById('courseList').innerHTML =
            '<p style="color: #ef4444;">Failed to load courses. Make sure the backend is running.</p>';
    }
}

// Display courses in sidebar
function displayCourses(courses) {
    const courseList = document.getElementById('courseList');

    if (courses.length === 0) {
        courseList.innerHTML = '<p>No courses available</p>';
        return;
    }

    courseList.innerHTML = courses.map(course => `
        <div class="course-item" data-course-id="${course.id}">
            <h3>${course.name}</h3>
            <div class="meta">
                <span>📚 ${course.module_count} modules</span>
                <span>| ${course.language}</span>
            </div>
        </div>
    `).join('');

    // Add click handlers
    document.querySelectorAll('.course-item').forEach(item => {
        item.addEventListener('click', () => loadCourseModules(item.dataset.courseId));
    });
}

// Load modules for a course
async function loadCourseModules(courseId) {
    try {
        const courseData = await api.getCourseModules(courseId);
        currentCourse = courseData;
        displayModules(courseData);
    } catch (error) {
        console.error('Failed to load course modules:', error);
    }
}

// Display modules and lessons
function displayModules(courseData) {
    const courseList = document.getElementById('courseList');

    let html = `
        <button onclick="loadCourses()" class="btn-back">← Back to Courses</button>
        <h2>${courseData.course_name}</h2>
    `;

    courseData.modules.forEach(module => {
        html += `
            <div class="module">
                <h3 style="color: var(--secondary-color); margin: 1rem 0 0.5rem;">${module.name}</h3>
                <div class="lesson-list">
        `;

        module.lessons.forEach(lesson => {
            const difficultyClass = lesson.difficulty.toLowerCase();
            html += `
                <div class="lesson-item" data-lesson-id="${lesson.id}">
                    <span class="difficulty-badge ${difficultyClass}">${lesson.difficulty}</span>
                    ${lesson.title}
                </div>
            `;
        });

        html += `
                </div>
            </div>
        `;
    });

    courseList.innerHTML = html;

    // Add lesson click handlers
    document.querySelectorAll('.lesson-item').forEach(item => {
        item.addEventListener('click', () => loadLesson(item.dataset.lessonId));
    });
}

// Load a specific lesson
async function loadLesson(lessonId) {
    try {
        // Show loading
        document.getElementById('lessonContent').innerHTML = '<div class="loading">Generating lesson content with AI...</div>';

        const lessonData = await api.getLesson(lessonId);
        currentLesson = lessonData;

        displayLesson(lessonData);
        switchTab('learn');
    } catch (error) {
        console.error('Failed to load lesson:', error);
        document.getElementById('lessonContent').innerHTML =
            '<p style="color: #ef4444;">Failed to load lesson content.</p>';
    }
}

// Display lesson content
function displayLesson(lessonData) {
    const { lesson_info, content } = lessonData;

    // Update header
    document.getElementById('lessonTitle').textContent = lesson_info.title;
    document.getElementById('difficultyBadge').textContent = lesson_info.difficulty;
    document.getElementById('difficultyBadge').className = `difficulty-badge ${lesson_info.difficulty.toLowerCase()}`;
    document.getElementById('keywords').textContent = lesson_info.keywords.join(', ');

    // Build lesson content HTML
    let contentHTML = `
        <section>
            <h2>📖 What You'll Learn</h2>
            <p>${content.explanation}</p>
        </section>

        <section>
            <h2>🌍 Real-World Analogy</h2>
            <div class="feature-card">
                <p>${content.analogy}</p>
            </div>
        </section>

        <section>
            <h2>💡 Why It Matters</h2>
            <p>${content.why_it_matters}</p>
        </section>

        <section>
            <h2>💻 Code Example</h2>
            <pre><code>${escapeHtml(content.code_example)}</code></pre>
        </section>

        <section>
            <h2>🔍 Step-by-Step Breakdown</h2>
            <ol>
                ${content.breakdown.map(step => `<li>${step}</li>`).join('')}
            </ol>
        </section>

        <section>
            <h2>⚠️ Common Mistakes</h2>
            <ul>
                ${content.common_mistakes.map(mistake => `<li>${mistake}</li>`).join('')}
            </ul>
        </section>
    `;

    document.getElementById('lessonContent').innerHTML = contentHTML;

    // Update practice challenge
    if (content.practice_challenge) {
        document.getElementById('challengeDescription').textContent = content.practice_challenge.description;
        setEditorCode(content.practice_challenge.starter_code || CONFIG.CODE_TEMPLATES.python);
    }
}

// Load quiz for current lesson
async function loadQuiz() {
    if (!currentLesson) return;

    try {
        const quizData = await api.getQuiz(currentLesson.lesson_info.id);
        displayQuiz(quizData.quiz);
    } catch (error) {
        console.error('Failed to load quiz:', error);
    }
}

// Display quiz
function displayQuiz(quiz) {
    const quizContainer = document.getElementById('quizContent');

    if (!quiz.questions || quiz.questions.length === 0) {
        quizContainer.innerHTML = '<p>No quiz available for this lesson.</p>';
        return;
    }

    let html = '<h2>🎯 Test Your Knowledge</h2>';

    quiz.questions.forEach((q, index) => {
        html += `
            <div class="quiz-question" data-question-index="${index}">
                <h3>Question ${index + 1}</h3>
                <p>${q.question}</p>
                <div class="quiz-options">
                    ${Object.entries(q.options).map(([key, value]) => `
                        <div class="quiz-option" data-answer="${key}">
                            <strong>${key}:</strong> ${value}
                        </div>
                    `).join('')}
                </div>
                <div class="quiz-explanation" style="display: none; margin-top: 1rem; padding: 1rem; background: var(--bg-tertiary); border-radius: 6px;">
                    <strong>Explanation:</strong> ${q.explanation}
                </div>
            </div>
        `;
    });

    quizContainer.innerHTML = html;

    // Add option click handlers
    document.querySelectorAll('.quiz-option').forEach(option => {
        option.addEventListener('click', handleQuizAnswer);
    });
}

// Handle quiz answer selection
function handleQuizAnswer(event) {
    const option = event.currentTarget;
    const questionDiv = option.closest('.quiz-question');
    const questionIndex = questionDiv.dataset.questionIndex;
    const selectedAnswer = option.dataset.answer;

    // TODO: Check if answer is correct (need to store correct answers)
    option.classList.add('selected');

    // Show explanation
    questionDiv.querySelector('.quiz-explanation').style.display = 'block';
}

// Load mini-game for current lesson
async function loadGame() {
    if (!currentLesson) return;

    try {
        const gameData = await api.getGame(currentLesson.lesson_info.id);
        displayGame(gameData.game);
    } catch (error) {
        console.error('Failed to load game:', error);
    }
}

// Display mini-game
function displayGame(game) {
    const gameContainer = document.getElementById('gameContent');

    if (!game.game_name) {
        gameContainer.innerHTML = '<p>No mini-game available for this lesson.</p>';
        return;
    }

    let html = `
        <h2>🎮 ${game.game_name}</h2>
        <p>${game.description}</p>

        <div class="feature-card">
            <h3>📋 Instructions</h3>
            <ol>
                ${game.instructions.map(instruction => `<li>${instruction}</li>`).join('')}
            </ol>
        </div>

        <div class="feature-card">
            <h3>🎯 Learning Goal</h3>
            <p>${game.learning_goal}</p>
        </div>

        <div style="margin-top: 2rem;">
            <h3>💻 Game Code</h3>
            <pre><code>${escapeHtml(game.starter_code)}</code></pre>
            <button onclick="setEditorCode(\`${game.starter_code.replace(/`/g, '\\`')}\`); switchTab('practice')" class="btn-primary">
                Try It in Editor →
            </button>
        </div>
    `;

    gameContainer.innerHTML = html;
}

// Execute code
async function executeCode() {
    const code = getEditorCode();
    const language = document.getElementById('languageSelect').value;
    const outputElement = document.getElementById('codeOutput');

    outputElement.textContent = 'Running code...';

    try {
        // TODO: Implement actual code execution via backend
        // For now, just show a placeholder
        outputElement.textContent = `Code execution coming soon!\n\nYour ${language} code:\n${code}`;
    } catch (error) {
        outputElement.textContent = `Error: ${error.message}`;
    }
}

// Tab switching
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelector(`.tab[data-tab="${tabName}"]`).classList.add('active');

    // Update tab panes
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    document.getElementById(`${tabName}Tab`).classList.add('active');

    // Load content if needed
    if (tabName === 'quiz' && currentLesson) {
        loadQuiz();
    } else if (tabName === 'game' && currentLesson) {
        loadGame();
    }
}

// Set up event listeners
function setupEventListeners() {
    // Tab switching
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => switchTab(tab.dataset.tab));
    });

    // Language selector
    document.getElementById('languageSelect').addEventListener('change', (e) => {
        changeEditorLanguage(e.target.value);
    });

    // Run code button
    document.getElementById('runCode').addEventListener('click', executeCode);

    // Mark complete button
    document.getElementById('markComplete').addEventListener('click', () => {
        if (currentLesson) {
            alert('Lesson marked as complete! 🎉');
            // TODO: Save progress to backend
            document.getElementById('lessonProgress').style.width = '100%';
        }
    });
}

// Utility function
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
