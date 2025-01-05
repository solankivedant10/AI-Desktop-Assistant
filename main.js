function sendCommand() {
    const input = document.getElementById('user-input');
    const command = input.value.trim();
    
    if (command === '') return;

    addMessageToChat('You: ' + command, 'user-message');

    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command: command })
    })
    .then(response => response.json())
    .then(data => {
        addMessageToChat('Assistant: ' + data.response, 'assistant-message');
    })
    .catch(error => {
        console.error('Error:', error);
        addMessageToChat('Assistant: Sorry, there was an error processing your request.', 'assistant-message');
    });

    input.value = '';
}

function addMessageToChat(message, className) {
    const chatHistory = document.getElementById('chat-history');
    const messageElement = document.createElement('div');
    messageElement.className = `message ${className}`;
    messageElement.textContent = message;
    chatHistory.appendChild(messageElement);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    // Add fade-in animation
    messageElement.style.opacity = '0';
    messageElement.style.transform = 'translateY(20px)';
    setTimeout(() => {
        messageElement.style.transition = 'opacity 0.3s, transform 0.3s';
        messageElement.style.opacity = '1';
        messageElement.style.transform = 'translateY(0)';
    }, 10);
}

function useCommand(command) {
    document.getElementById('user-input').value = command;
    sendCommand();
}

// Allow Enter key to send messages
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendCommand();
    }
});

// Add welcome message when page loads
window.onload = function() {
    addMessageToChat('Assistant: Hello! How can I help you today? Try the suggestion chips below or type your own command.', 'assistant-message');
}; 