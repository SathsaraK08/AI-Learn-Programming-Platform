// API service for communicating with backend

class APIService {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;

        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Request failed:', error);
            throw error;
        }
    }

    async getCourses() {
        return this.request(CONFIG.API_ENDPOINTS.courses);
    }

    async getCourseModules(courseId) {
        return this.request(CONFIG.API_ENDPOINTS.courseModules(courseId));
    }

    async getLesson(lessonId, regenerate = false) {
        const params = regenerate ? '?regenerate=true' : '';
        return this.request(CONFIG.API_ENDPOINTS.lesson(lessonId) + params);
    }

    async getQuiz(lessonId, numQuestions = 5) {
        return this.request(`${CONFIG.API_ENDPOINTS.quiz(lessonId)}?num_questions=${numQuestions}`);
    }

    async getGame(lessonId) {
        return this.request(CONFIG.API_ENDPOINTS.game(lessonId));
    }

    async executeCode(code, language) {
        return this.request(CONFIG.API_ENDPOINTS.executeCode, {
            method: 'POST',
            body: JSON.stringify({ code, language })
        });
    }

    async getUserProgress() {
        return this.request(CONFIG.API_ENDPOINTS.userProgress);
    }
}

// Global API instance
const api = new APIService(CONFIG.API_BASE_URL);
