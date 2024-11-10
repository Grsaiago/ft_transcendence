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
        this.chatManager.chatSocket.addEventListener("message", this.handleMessageUI);
        var chatList = document.getElementsByClassName('friend online');
        for (var i = 0; i < chatList.length; i++) {
            chatList[i].addEventListener('click', this.handleChatChange);
        }
    }

    removeUIEventHandlers() {
        console.log('Removing chat event handlers...');
        this.chatManager.chatSocket.removeEventListener("message", this.handleMessageUI);
        var chatList = document.getElementsByClassName('friend online');
        for (var i = 0; i < chatList.length; i++) {
            chatList[i].removeEventListener('click', this.handleChatChange);
        }
    }

    handlerUI() {
        console.log('Chat.js handler called!!');
    }

    chatWindowIsOpen() {
        return document.getElementById('chat-messages') !== null;
    }

    handleMessageUI(event) {
        var data = JSON.parse(event.data);
        if (this.chatWindowIsOpen() && data.chat_id == this.currentChatId)
            this.displayMessage(this.chatManager.chatHistory.get(data.chat_id).at(-1));
    }

    handleChatChange(event) {
        this.currentChatId = event.currentTarget.getAttribute('chat_id');
        console.log('Chat changed. CurrentChatId: ' + this.currentChatId);
        this.atualizaChat();
    }

    displayMessage(messageInfo) {
        const messagesContainer = document.getElementById('chat-messages');
        const sender = document.createElement('p');
        const newMessage = document.createElement('p');
        const msgTime = new Date(messageInfo.time);
        sender.textContent = messageInfo.sender + ', ' + msgTime.getHours() + ':' + msgTime.getMinutes();  // FIX/IMPLEMENT: diplay minutes with two digits
        newMessage.textContent = messageInfo.message;
        sender.classList.add('chat-msg-user-time');
        newMessage.classList.add('chat-msg-content');
        messagesContainer.appendChild(sender);
        messagesContainer.appendChild(newMessage);
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
