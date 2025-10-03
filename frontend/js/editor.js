// Monaco Editor initialization and management

let monacoEditor = null;

function initializeMonacoEditor() {
    require.config({ paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs' } });

    require(['vs/editor/editor.main'], function () {
        const editorContainer = document.getElementById('codeEditor');

        monacoEditor = monaco.editor.create(editorContainer, {
            value: CONFIG.CODE_TEMPLATES[CONFIG.DEFAULT_LANGUAGE],
            language: CONFIG.DEFAULT_LANGUAGE,
            theme: CONFIG.MONACO_THEMES.dark,
            automaticLayout: true,
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            wordWrap: 'on',
            tabSize: 4
        });

        console.log('✅ Monaco Editor initialized');
    });
}

function changeEditorLanguage(language) {
    if (!monacoEditor) return;

    const currentValue = monacoEditor.getValue();
    const isEmpty = currentValue.trim() === '' ||
                    Object.values(CONFIG.CODE_TEMPLATES).includes(currentValue.trim());

    if (isEmpty) {
        monacoEditor.setValue(CONFIG.CODE_TEMPLATES[language] || '');
    }

    monaco.editor.setModelLanguage(monacoEditor.getModel(), language);
}

function getEditorCode() {
    return monacoEditor ? monacoEditor.getValue() : '';
}

function setEditorCode(code) {
    if (monacoEditor) {
        monacoEditor.setValue(code);
    }
}
