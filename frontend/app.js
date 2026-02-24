document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const startBtn = document.getElementById('start-btn');
    const modelSelect = document.getElementById('model-select');
    const languageSelect = document.getElementById('language-select');
    const progressContainer = document.getElementById('progress-container');
    const progressFill = document.getElementById('progress-fill');
    const statusText = document.getElementById('status-text');
    const resultArea = document.getElementById('result-area');
    const transcriptEditor = document.getElementById('transcript-editor');
    const exportBtn = document.getElementById('export-btn');
    const themeToggle = document.getElementById('theme-toggle');
    const systemInfo = document.getElementById('system-info');
    const toastContainer = document.getElementById('toast-container');

    let selectedFile = null;
    let currentJobId = null;
    let pollingInterval = null;

    // Theme Toggle
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.style.getPropertyValue('color-scheme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.style.setProperty('color-scheme', newTheme);
    });

    // File Selection
    dropZone.addEventListener('click', () => fileInput.click());
    
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        if (e.dataTransfer.files.length > 0) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        selectedFile = file;
        fileInfo.textContent = `Ausgewählt: ${file.name} (${(file.size / (1024 * 1024)).toFixed(2)} MB)`;
        startBtn.disabled = false;
        showToast(`Datei ${file.name} ausgewählt.`);
    }

    // Start Transcription
    startBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('model', modelSelect.value);
        if (languageSelect.value) {
            formData.append('language', languageSelect.value);
        }

        startBtn.disabled = true;
        progressContainer.style.display = 'block';
        statusText.textContent = 'Lade Datei hoch...';
        progressFill.style.width = '0%';
        resultArea.style.display = 'none';

        try {
            const response = await fetch('/api/transcribe', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Upload fehlgeschlagen');

            const data = await response.json();
            currentJobId = data.job_id;
            startPolling();
            showToast('Transkription gestartet.');
        } catch (error) {
            showToast(`Fehler: ${error.message}`, 'error');
            startBtn.disabled = false;
        }
    });

    function startPolling() {
        if (pollingInterval) clearInterval(pollingInterval);
        pollingInterval = setInterval(async () => {
            try {
                const response = await fetch(`/api/transcribe/status/${currentJobId}`);
                if (!response.ok) throw new Error('Status-Abfrage fehlgeschlagen');

                const data = await response.json();
                
                progressFill.style.width = `${data.progress}%`;
                
                if (data.status === 'processing') {
                    statusText.textContent = `Verarbeite... ${data.progress}%`;
                    if (data.current_text) {
                        // Optional: show live text
                    }
                } else if (data.status === 'completed') {
                    clearInterval(pollingInterval);
                    statusText.textContent = 'Abgeschlossen!';
                    showResult(data.result);
                    showToast('Transkription abgeschlossen.');
                    startBtn.disabled = false;
                } else if (data.status === 'failed') {
                    clearInterval(pollingInterval);
                    statusText.textContent = `Fehler: ${data.error}`;
                    showToast(`Transkription fehlgeschlagen: ${data.error}`, 'error');
                    startBtn.disabled = false;
                }
            } catch (error) {
                console.error(error);
            }
        }, 2000);
    }

    function showResult(result) {
        resultArea.style.display = 'block';
        transcriptEditor.value = result.text;
        transcriptEditor.scrollIntoView({ behavior: 'smooth' });
    }

    // Export
    exportBtn.addEventListener('click', async () => {
        const formData = new FormData();
        formData.append('job_id', currentJobId);
        formData.append('edited_text', transcriptEditor.value);

        try {
            const response = await fetch('/api/export', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Export fehlgeschlagen');

            const data = await response.json();
            
            // Download the file
            const blob = new Blob([data.content], { type: 'text/markdown' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = data.filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showToast(`Datei ${data.filename} wurde gespeichert.`);
        } catch (error) {
            showToast(`Export-Fehler: ${error.message}`, 'error');
        }
    });

    // System Info & Models
    async function loadSystemInfo() {
        try {
            const response = await fetch('/api/system');
            const data = await response.json();
            systemInfo.textContent = `System: ${data.cpu_cores} Cores, ${data.ram_total_gb} GB RAM | GPU: ${data.gpu_detected ? data.gpu_name : 'Nicht erkannt'}`;
        } catch (error) {
            systemInfo.textContent = 'Systeminformationen konnten nicht geladen werden.';
        }
    }

    async function loadModels() {
        try {
            const response = await fetch('/api/models');
            const models = await response.json();
            
            // Update model select with local status
            const options = modelSelect.options;
            for (let i = 0; i < options.length; i++) {
                const model = models.find(m => m.name === options[i].value);
                if (model && model.local) {
                    options[i].text += ' (Lokal verfügbar)';
                }
            }
        } catch (error) {
            console.error('Modelle konnten nicht geladen werden.');
        }
    }

    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        toastContainer.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 500);
        }, 3000);
    }

    loadSystemInfo();
    loadModels();
});
