const uploadView = document.getElementById('uploadView');
const chatView = document.getElementById('chatView');
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('pdfFile');
const statusDiv = document.getElementById('status');
const chatBox = document.getElementById('chatBox');
const questionInput = document.getElementById('question');
const subheading = document.getElementById('subheading');

function showChat() {
    uploadView.style.display = 'none';
    chatView.style.display = 'flex';
    subheading.innerText = "Analyzing your document in real-time.";
}

function showUpload() {
    uploadView.style.display = 'block';
    chatView.style.display = 'none';
    subheading.innerText = "Upload a research paper to start an AI-powered analysis.";
    statusDiv.innerText = "";
    chatBox.innerHTML = `
        <div class="message ai">
            <span class="message-label">Gemini AI</span>
            <div>Hello! I've indexed your paper. What would you like to know about it?</div>
        </div>`;
}

// File Selection
fileInput.addEventListener('change', (e) => handleFiles(e.target.files[0]));

// Drag and Drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = "#4a90e2";
});

dropZone.addEventListener('dragleave', () => {
    dropZone.style.borderColor = "#cbd5e0";
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    handleFiles(e.dataTransfer.files[0]);
});

function handleFiles(file) {
    if (file && (file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf'))) {
        uploadFile(file);
    } else {
        statusDiv.innerText = "Error: Please upload a valid PDF.";
        statusDiv.style.color = "red";
    }
}

async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    statusDiv.innerText = "Processing document...";
    statusDiv.style.color = "var(--primary-color)";

    try {
        const response = await fetch('/ingest', { method: 'POST', body: formData });
        if (response.ok) {
            statusDiv.innerText = "Success! Entering chat...";
            setTimeout(showChat, 1000);
        } else {
            statusDiv.innerText = "Upload failed.";
        }
    } catch (e) {
        statusDiv.innerText = "Server connection error.";
    }
}

async function askQuestion() {
    const question = questionInput.value.trim();
    if (!question) return;

    addMessage(question, 'user');
    questionInput.value = '';

    const loadingId = addLoading();

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });
        const result = await response.json();
        const loader = document.getElementById(loadingId);
        if (loader) loader.remove();

        if (result.error) {
            addMessage("Error: " + result.error, 'ai');
        } else {
            addMessage(result.answer, 'ai', result.sources);
        }
    } catch (e) {
        if (document.getElementById(loadingId)) document.getElementById(loadingId).remove();
        addMessage("Sorry, I couldn't reach the server.", 'ai');
    }
}

function formatMarkdown(text) {
    // Convert markdown to HTML
    let html = text
        // Bold: **text** or __text__
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/__(.*?)__/g, '<strong>$1</strong>')
        // Italic: *text* or _text_
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        // Headers: ## Header
        .replace(/^### (.*$)/gm, '<h4>$1</h4>')
        .replace(/^## (.*$)/gm, '<h3>$1</h3>')
        .replace(/^# (.*$)/gm, '<h2>$1</h2>')
        // Bullet points: - item or * item
        .replace(/^[\-\*] (.*)$/gm, '<li>$1</li>')
        // Numbered lists: 1. item
        .replace(/^\d+\. (.*)$/gm, '<li>$1</li>')
        // Line breaks
        .replace(/\n/g, '<br>');

    // Wrap consecutive <li> in <ul>
    html = html.replace(/(<li>.*?<\/li>)(<br>)?(<li>)/g, '$1$3');
    html = html.replace(/(<li>.*?<\/li>)/g, '<ul>$1</ul>');
    html = html.replace(/<\/ul><ul>/g, '');

    return html;
}

function addMessage(text, sender, sources = []) {
    const div = document.createElement('div');
    div.className = `message ${sender}`;

    let sourceHtml = "";
    if (sources && sources.length > 0) {
        const uniqueSections = [...new Set(sources.map(s => s.section))];
        sourceHtml = `<div class="sources">📚 Sources: ${uniqueSections.map(s => `<span class="source-tag">${s}</span>`).join(' ')}</div>`;
    }

    const formattedText = sender === 'ai' ? formatMarkdown(text) : text;

    div.innerHTML = `<span class="message-label">${sender === 'user' ? 'You' : 'Research AI'}</span>
                     <div class="message-content">${formattedText}</div>
                     ${sourceHtml}`;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addLoading() {
    const id = 'loading-' + Date.now();
    const div = document.createElement('div');
    div.className = 'message ai';
    div.id = id;
    div.innerHTML = `<span class="message-label">Gemini AI</span>
                     <div class="typing-indicator"><span></span> <span></span> <span></span></div>`;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    return id;
}

questionInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') askQuestion(); });