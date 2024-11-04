document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('chat-form');
    const input = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting the traditional way

        const userMessage = input.value;
        if (userMessage.trim() === '') return; // Do not send empty messages
        appendMessage('You: ' + userMessage); // Display user message

        // Send the message to the Flask backend
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage('Bot: ' + data.response); // Display bot response
        })
        .catch(error => {
            console.error('Error:', error);
        });

        input.value = ''; // Clear the input field
    });

    function appendMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
    }
});
