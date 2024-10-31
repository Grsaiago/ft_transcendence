import Profile from "./views/profile.js";
import Chat from "./views/chat.js";

let currentChatId = null;

const chatHistory = new Map();

const navigateTo = url => {
    history.pushState(null, null, url);
    router();
};

const router = async () => {
    const routes = [
        {path: "/profile/", view: Profile },
        {path: "/chat/", view: Chat },
    ];

    //Test each route for potential match
    const potentialMatches = routes.map(route => {
        return {
            route: route,
            isMatch: location.pathname === route.path
        };
    });

    let match = potentialMatches.find(potentialMatch => potentialMatch.isMatch);

    if (!match) {
        match = {
            route: routes[0],
            isMatch: true
        };
    }

    const view = new match.route.view();

    document.querySelector("#app").innerHTML = await view.getHtml();

};

window.addEventListener("popstate", router);

document.getElementById

document.addEventListener("DOMContentLoaded", () => {
    console.log("Página carregada, chamando router()");

    document.body.addEventListener("click", e => {
        if (e.target.matches("[data-link]")) {
            e.preventDefault();
            navigateTo(e.target.href);
        }

        else if (e.target.matches("[data-send-msg]")) {
            console.log('Send message clicked!');
            
            const messageInputDom = document.getElementById('chat-message-input');
            if (!messageInputDom) {
                console.error('Message input field not found.');
                return;
            }
        
            const message = messageInputDom.value;
        
            if (chatSocket.readyState === WebSocket.OPEN) {
                chatSocket.send(JSON.stringify({
                    'message': message,
                    'chat_id': currentChatId
                }));
                messageInputDom.value = '';
            } else {
                console.log('WebSocket is not open.');
            }
        }

        else if (e.target.matches("[data-chat]")) {
            console.log(e.target);
            currentChatId = e.target.getAttribute('chat_id');
            console.log('Chat changed. CurrentChatId: ' + currentChatId);
            // check if chatHistory has the chatId
            atualizaChat(currentChatId);
        }
    });

    router();
});

console.log('Chat.js loaded');

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
);

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

// chatSocket.onmessage = handleMessage;  // Correct way to assign the message handler

chatSocket.addEventListener("message", (event) => {
    console.log("message received: " + event.data +"\ncalling handleMessage ...");
    handleMessage(event);
});

const handleMessage = (event) => {
    console.log("handleMessage() called");
    
    try {
        var data = JSON.parse(event.data);  // Fix typo: JSON.parse() should be called on event.data
        console.log(data);
        let messageInfo = {
            'sender': data.sender,
            'message': data.message,
            'time': Date.now()
        }
        displayMessage(messageInfo);
        atualizaHistorico(messageInfo);
    } catch (err) {
        console.error("Error parsing WebSocket message: ", err);
    }
};

const displayMessage = (messageInfo, time) => {
    const messagesContainer = document.getElementById('chat-messages');
    const sender = document.createElement('p');
    const newMessage = document.createElement('p');
    const msgTime = new Date(messageInfo.time);
    sender.textContent = messageInfo.sender + ', ' + msgTime.getHours() + ':' + msgTime.getMinutes();  // Assuming messageInfo has a 'message' field
    newMessage.textContent = messageInfo.message;  // Assuming data has a 'message' field
    sender.classList.add('chat-msg-user-time');
    newMessage.classList.add('chat-msg-content');
    messagesContainer.appendChild(sender);
    messagesContainer.appendChild(newMessage);
}

const atualizaHistorico = (messageInfo) => {
    let chatMessages = chatHistory.get(currentChatId);
    if (!chatMessages) {
        chatMessages = [];
        chatHistory.set(currentChatId, chatMessages);
    }
    chatMessages.push(messageInfo);
}

const atualizaChat = (currentChatId) => {
    limpaChat();
    if (chatHistory.has(currentChatId)) {
        loadChatHistory(chatHistory.get(currentChatId));
    }
    else {
        console.log('Histórico não encontrado. Criando novo histórico...');
        chatHistory.set(currentChatId, new Array());
    }
}

const loadChatHistory = (chatHistory) => {
    console.log('Loading chat history...');
    chatHistory.forEach(message => {
        displayMessage(message);
    });
}

const limpaChat = () => {
    console.log('Limpando chat...');
    const messagesContainer = document.getElementById('chat-messages');
    messagesContainer.innerHTML = '';
}