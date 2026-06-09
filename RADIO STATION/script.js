// Show typing indicator when the user is typing
function showTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    const chatInput = document.getElementById('chatInput');

    if (chatInput.value.length > 0) {
        typingIndicator.style.display = 'inline-block'; // Show typing indicator
    } else {
        typingIndicator.style.display = 'none'; // Hide typing indicator when no input
    }
}

// Function to simulate sending a message
function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const messages = document.getElementById('messages');
    const typingIndicator = document.getElementById('typingIndicator');

    if (chatInput.value.trim() !== "") {
        // Add the message to the chat
        const newMessage = document.createElement('p');
        newMessage.textContent = chatInput.value;
        messages.appendChild(newMessage);

        // Clear the input
        chatInput.value = '';

        // Hide the typing indicator
        typingIndicator.style.display = 'none';
    }
}


// Simulate broadcasting and receiving typing status
let typingTimeout;

function userTyping() {
    const typingIndicator = document.getElementById('typingIndicator');
    const chatInput = document.getElementById('chatInput');
    
    // Display typing indicator locally
    if (chatInput.value.length > 0) {
        typingIndicator.style.display = 'inline-block';
        clearTimeout(typingTimeout);
        
        // Simulate broadcasting typing status
        broadcastTypingStatus(true);
        
        // Hide typing indicator after a delay if no more typing
        typingTimeout = setTimeout(() => {
            typingIndicator.style.display = 'none';
            broadcastTypingStatus(false);
        }, 1000);
    } else {
        typingIndicator.style.display = 'none';
        broadcastTypingStatus(false);
    }
}

function broadcastTypingStatus(isTyping) {
    // Simulate sending typing status to server
    console.log(`User is ${isTyping ? 'typing...' : 'not typing.'}`);
    // Here you would send the status to your server
}

// Simulate receiving typing status from server
function receiveTypingStatus(isTyping) {
    const typingIndicator = document.getElementById('typingIndicator');
    if (isTyping) {
        typingIndicator.style.display = 'inline-block';
    } else {
        typingIndicator.style.display = 'none';
    }
}

// Function to simulate sending a message
function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const messages = document.getElementById('messages');
    const typingIndicator = document.getElementById('typingIndicator');

    if (chatInput.value.trim() !== "") {
        // Add the message to the chat
        const newMessage = document.createElement('p');
        newMessage.textContent = chatInput.value;
        messages.appendChild(newMessage);

        // Clear the input
        chatInput.value = '';

        // Hide the typing indicator
        typingIndicator.style.display = 'none';
        broadcastTypingStatus(false);
    }
}
