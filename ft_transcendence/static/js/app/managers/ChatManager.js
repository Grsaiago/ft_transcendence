export default class ChatManager {
    constructor() {
        if (ChatManager.instance) {
            return ChatManager.instance;
        }

        this.chatHistory = new Map();
        this.chatSocket = this.initializeSocket();

        this.handleMessage = this.handleMessage.bind(this);

        ChatManager.instance = this; // Enforce singleton pattern
    }

    initializeSocket() {
        const chatScoket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
        );

        return chatScoket;
    }

    loadEventHandlers() {
        console.log('Loading chat manager event handlers...');
        this.chatSocket.addEventListener("message", this.handleMessage);
        this.chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
            // Try to reconnect
        };
    }

    handleMessage(event) {
        console.log("handleMessage() called");
        try {
            var data = JSON.parse(event.data);  // Fix typo: JSON.parse() should be called on event.data
            let messageInfo = {
                ...data,
                'time': Date.now()
            }
            this.atualizaHistorico(messageInfo);
            //lançar evento pra atualizar para disparar Chat.handleMessageUI e evitar data race
        } catch (err) {
            console.error("Error parsing WebSocket message: ", err);
        }
    };

    atualizaHistorico(messageInfo) {
        let chatMessages = this.chatHistory.get(messageInfo.chat_id);
        if (!chatMessages) {
            chatMessages = [];
            this.chatHistory.set(messageInfo.chat_id, chatMessages);
        }
        chatMessages.push(messageInfo);
    }

}