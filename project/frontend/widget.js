(function() {
    // Get client_id from query parameters
    const urlParams = new URLSearchParams(window.location.search);
    const clientId = urlParams.get('client_id');

    if (!clientId) {
        console.error("Chatbot client_id is missing.");
        return;
    }

    // Create Chat Widget Elements
    const chatContainer = document.createElement('div');
    chatContainer.id = 'chatbot-container';
    chatContainer.style.position = 'fixed';
    chatContainer.style.bottom = '20px';
    chatContainer.style.right = '20px';
    chatContainer.style.width = '300px';
    chatContainer.style.height = '400px';
    chatContainer.style.border = '1px solid #ccc';
    chatContainer.style.borderRadius = '10px';
    chatContainer.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
    chatContainer.style.backgroundColor = '#fff';
    chatContainer.style.display = 'flex';
    chatContainer.style.flexDirection = 'column';
    chatContainer.style.zIndex = '1000';

    // Header
    const chatHeader = document.createElement('div');
    chatHeader.id = 'chatbot-header';
    chatHeader.style.backgroundColor = '#007bff';
    chatHeader.style.color = '#fff';
    chatHeader.style.padding = '10px';
    chatHeader.style.borderTopLeftRadius = '10px';
    chatHeader.style.borderTopRightRadius = '10px';
    chatHeader.style.display = 'flex';
    chatHeader.style.alignItems = 'center';

    // Logo
    const logo = document.createElement('img');
    logo.id = 'chatbot-logo';
    logo.src = 'https://yourdomain.com/default-logo.png'; // Default logo
    logo.alt = 'Chatbot Logo';
    logo.style.width = '30px';
    logo.style.height = '30px';
    logo.style.marginRight = '10px';
    chatHeader.appendChild(logo);

    // Title
    const title = document.createElement('span');
    title.innerText = 'Chatbot';
    chatHeader.appendChild(title);

    // Close Button
    const closeButton = document.createElement('button');
    closeButton.innerText = '×';
    closeButton.style.marginLeft = 'auto';
    closeButton.style.background = 'none';
    closeButton.style.border = 'none';
    closeButton.style.color = '#fff';
    closeButton.style.fontSize = '20px';
    closeButton.style.cursor = 'pointer';
    closeButton.onclick = () => {
        chatContainer.style.display = 'none';
    };
    chatHeader.appendChild(closeButton);

    chatContainer.appendChild(chatHeader);

    // Chat History
    const chatHistory = document.createElement('div');
    chatHistory.id = 'chatbot-history';
    chatHistory.style.flex = '1';
    chatHistory.style.padding = '10px';
    chatHistory.style.overflowY = 'auto';
    chatContainer.appendChild(chatHistory);

    // Input Area
    const inputArea = document.createElement('div');
    inputArea.style.display = 'flex';
    inputArea.style.padding = '10px';
    inputArea.style.borderTop = '1px solid #ccc';

    const inputField = document.createElement('input');
    inputField.type = 'text';
    inputField.placeholder = 'Type your message...';
    inputField.style.flex = '1';
    inputField.style.padding = '10px';
    inputField.style.border = '1px solid #ccc';
    inputField.style.borderRadius = '5px';
    inputField.id = 'chatbot-input';
    inputArea.appendChild(inputField);

    const sendButton = document.createElement('button');
    sendButton.innerText = 'Send';
    sendButton.style.marginLeft = '10px';
    sendButton.style.padding = '10px 20px';
    sendButton.style.border = 'none';
    sendButton.style.backgroundColor = '#007bff';
    sendButton.style.color = '#fff';
    sendButton.style.borderRadius = '5px';
    sendButton.style.cursor = 'pointer';
    sendButton.onclick = sendMessage;
    inputArea.appendChild(sendButton);

    chatContainer.appendChild(inputArea);

    // Initializing the chat widget
    document.body.appendChild(chatContainer);

    // Fetch Chatbot Configuration
    fetch(`https://yourbackend.com/api/chatbots/${clientId}`)
        .then(response => response.json())
        .then(config => {
            // Apply UI Customizations
            if (config.ui_settings) {
                if (config.ui_settings.color) {
                    chatHeader.style.backgroundColor = config.ui_settings.color;
                }
                if (config.ui_settings.logo_url) {
                    logo.src = config.ui_settings.logo_url;
                }
            }
        })
        .catch(error => {
            console.error("Error fetching chatbot configuration:", error);
        });

    // Send Message Function
    function sendMessage() {
        const message = inputField.value.trim();
        if (!message) return;

        appendMessage('user', message);
        inputField.value = '';

        // Send to Backend API
        fetch(`https://yourbackend.com/api/chat/${clientId}/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getToken() // Implement token retrieval
            },
            body: JSON.stringify({ user_input: message })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage('bot', data.response);
        })
        .catch(error => {
            console.error("Error sending message:", error);
            appendMessage('bot', "I'm sorry, something went wrong.");
        });
    }

    // Append Message to Chat History
    function appendMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message';
        messageDiv.innerText = message;
        messageDiv.style.marginBottom = '10px';
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    // Function to retrieve JWT token (implement as needed)
    function getToken() {
        // For simplicity, you can prompt the user to enter a token or implement a more secure method
        return prompt("Please enter your Chatbot API token:");
    }
})();