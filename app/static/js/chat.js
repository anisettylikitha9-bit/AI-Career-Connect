/**
 * AI Career Connect - Chat Page JavaScript
 * Handles: AJAX message send, Voice input (STT), Text-to-Speech (TTS)
 */

document.addEventListener('DOMContentLoaded', () => {
    const chatBox   = document.getElementById('chat-box');
    const chatInput = document.getElementById('chat-input');
    const btnSend   = document.getElementById('btn-send');
    const btnMic    = document.getElementById('btn-mic');
    const btnNewSession = document.getElementById('btn-new-session');

    // ---- Send Message (AJAX) ----
    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        appendMessage('user', message);
        chatInput.value = '';

        try {
            const res = await fetch('/chat/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message }),
            });
            const data = await res.json();
            appendMessage('assistant', data.response);
        } catch (err) {
            appendMessage('assistant', 'Error: Could not reach the server.');
        }
    }

    btnSend.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // ---- Append message to chat box ----
    function appendMessage(role, text) {
        const wrapper = document.createElement('div');
        wrapper.className = `mb-3 ${role === 'user' ? 'text-end' : ''}`;

        const bubble = document.createElement('div');
        bubble.className = `d-inline-block p-2 rounded ${role === 'user' ? 'bg-primary text-white' : 'bg-light'}`;
        bubble.style.maxWidth = '75%';
        bubble.textContent = text;

        wrapper.appendChild(bubble);

        // Add TTS button for assistant messages
        if (role === 'assistant') {
            const speakBtn = document.createElement('button');
            speakBtn.className = 'btn btn-sm btn-link speak-btn';
            speakBtn.innerHTML = '<i class="bi bi-volume-up"></i>';
            speakBtn.addEventListener('click', () => speakText(text));
            wrapper.appendChild(document.createElement('br'));
            wrapper.appendChild(speakBtn);
        }

        chatBox.appendChild(wrapper);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // ---- New Session ----
    btnNewSession.addEventListener('click', async () => {
        await fetch('/chat/new-session');
        chatBox.innerHTML = '';
    });

    // ---- Voice Input (Speech-to-Text via browser API) ----
    btnMic.addEventListener('click', () => {
        if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
            alert('Speech recognition is not supported in this browser.');
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = false;

        recognition.onresult = (event) => {
            chatInput.value = event.results[0][0].transcript;
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
        };

        recognition.start();
        btnMic.classList.add('btn-danger');
        btnMic.classList.remove('btn-outline-danger');

        recognition.onend = () => {
            btnMic.classList.remove('btn-danger');
            btnMic.classList.add('btn-outline-danger');
        };
    });

    // ---- Text-to-Speech ----
    async function speakText(text) {
        try {
            const res = await fetch('/speech/tts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text }),
            });
            const data = await res.json();
            const audio = new Audio(data.audio_url);
            audio.play();
        } catch (err) {
            console.error('TTS error:', err);
        }
    }

    // Attach TTS to existing speak buttons
    document.querySelectorAll('.speak-btn').forEach((btn) => {
        btn.addEventListener('click', () => speakText(btn.dataset.text));
    });
});
