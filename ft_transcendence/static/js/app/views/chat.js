import AbstractView from "./abstractView.js";
import ChatManager from "../managers/ChatManager.js";

export default class Chat extends AbstractView {
    constructor() {
        super();
        this.setTitle("Chat");
        this.chatManager = new ChatManager();
        this.currentChatId = null;

        this.handleMessageUI = this.handleMessageUI.bind(this);
        this.atualizaChat = this.atualizaChat.bind(this);
        this.handleChatChange = this.handleChatChange.bind(this);
        this.sendMessage = this.sendMessage.bind(this);
        this.sendMessageButton = this.sendMessageButton.bind(this);
    }

    async getHtml() {
        try {
            const response = await fetch('/chat/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('Chat html fetched. Returning...');
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading login page</p>";
        }
    }

    bindUIEventHandlers() {
        console.log('Loading chat event handlers...');

        const chatList = document.querySelectorAll('[chat_id]');
        this.selectFirstChat(chatList[0]);
        for (var i = 0; i < chatList.length; i++) {
            chatList[i].addEventListener('click', this.handleChatChange);
        }

        var sendButton = document.getElementById('send-msg-button');
        sendButton.addEventListener('click', this.sendMessage);

        var input = document.getElementById('chat-message-input');
        input.addEventListener('keydown', this.sendMessageButton);

        document.addEventListener('chatMessageReceived', this.handleMessageUI);
    }
    
    selectFirstChat(chatDiv) {
        this.currentChatId = chatDiv.getAttribute('chat_id');
        this.highlightSlectedChat(chatDiv);
    }

    removeUIEventHandlers() {
        console.log('Removing chat event handlers...');

        var chatList = document.querySelectorAll('[chat_id]');
        for (var i = 0; i < chatList.length; i++) {
            chatList[i].removeEventListener('click', this.handleChatChange);
        }
        
        var sendButton = document.getElementById('send-msg-button');
        sendButton.removeEventListener('click', this.sendMessage);

        document.removeEventListener('chatMessageReceived', this.handleMessageUI);
    }

    chatWindowIsOpen() {
        return document.getElementById('chat-messages') !== null;
    }

    handleMessageUI(event) {
        if (this.chatWindowIsOpen() && event.detail == this.currentChatId)
            this.displayMessage(this.chatManager.chatHistory.get(event.detail).at(-1));
    }

    handleChatChange(event) {
        this.unhighlightPreviousChat();
        this.currentChatId = event.currentTarget.getAttribute('chat_id');
        console.log('Chat changed. CurrentChatId: ' + this.currentChatId);
        this.highlightSlectedChat(event.currentTarget);
        this.atualizaChat();
    }

    highlightSlectedChat(eventTarget) {
        const outerDiv = eventTarget.closest('.friend');
        if (outerDiv)
            outerDiv.classList.add('friend-selected');
    }

    unhighlightPreviousChat() {
        const selectedChat = document.querySelector('.friend-selected');
        if (selectedChat)
            selectedChat.classList.remove('friend-selected');
    }

    sendMessageButton(event) {
        if (event.key === "Enter")
            this.sendMessage();
    }

    sendMessage() {
        console.log('Send message clicked!');

        const messageInputDom = document.getElementById('chat-message-input');
        if (!messageInputDom) {
            console.error('Message input field not found.');
            return;
        }

        const message = messageInputDom.value;

        if (!message || !this.currentChatId) {
            return;
        }

        if (this.chatManager.chatSocket.readyState === WebSocket.OPEN) {
            this.chatManager.chatSocket.send(JSON.stringify({
                'message': message,
                'chat_id': this.currentChatId
            }));
            messageInputDom.value = '';
        } else {
            console.log('WebSocket is not open.');
        }
    }

    displayMessage(messageInfo) {
        const messagesContainer = document.getElementById('chat-messages');
        const sender = document.createElement('p');
        const newMessage = document.createElement('p');
        const msgTime = new Date(messageInfo.time);
        sender.textContent = messageInfo.sender + ', ' + String(msgTime.getHours()).padStart(2, '0') + ':' + String(msgTime.getMinutes()).padStart(2, '0');
        newMessage.textContent = messageInfo.message;
        sender.classList.add('chat-msg-user-time');
        newMessage.classList.add('chat-msg-content');
        messagesContainer.appendChild(sender);
        messagesContainer.appendChild(newMessage);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    atualizaChat() {
        this.limpaChat();
        if (this.chatManager.chatHistory.has(this.currentChatId)) {
            this.loadChatHistory(this.chatManager.chatHistory.get(this.currentChatId));
        }
        else {
            console.log('Histórico não encontrado. Criando novo histórico...');
            this.chatManager.chatHistory.set(this.currentChatId, new Array());
        }
    }
    
    loadChatHistory() {
        console.log('Loading chat history...');
        this.chatManager.chatHistory.get(this.currentChatId).forEach(message => {
            this.displayMessage(message);
        });
    }
    
    limpaChat() {
        console.log('Limpando chat...');
        const messagesContainer = document.getElementById('chat-messages');
        messagesContainer.innerHTML = '';
    }
}
