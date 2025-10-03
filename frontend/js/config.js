// Configuration for frontend application

const CONFIG = {
    API_BASE_URL: '',  // Empty for same-origin (served by backend)
    API_ENDPOINTS: {
        courses: '/api/lessons/courses',
        courseModules: (courseId) => `/api/lessons/courses/${courseId}/modules`,
        lesson: (lessonId) => `/api/lessons/${lessonId}`,
        quiz: (lessonId) => `/api/lessons/${lessonId}/quiz`,
        game: (lessonId) => `/api/lessons/${lessonId}/game`,
        executeCode: '/api/code/execute',
        userProgress: '/api/progress'
    },
    DEFAULT_LANGUAGE: 'python',
    MONACO_THEMES: {
        dark: 'vs-dark',
        light: 'vs-light'
    },
    CODE_TEMPLATES: {
        python: '# Write your Python code here\nprint("Hello, World!")\n',
        javascript: '// Write your JavaScript code here\nconsole.log("Hello, World!");\n',
        java: 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}\n'
    }
};
