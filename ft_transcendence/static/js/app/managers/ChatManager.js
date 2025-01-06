export default class ChatManager {
    constructor() {
        if (ChatManager.instance) {
            return ChatManager.instance;
        }

        this.chatHistory = new Map();
        this.chatSocket = this.tryConnectToChatSocket();

        ChatManager.instance = this; // Enforce singleton pattern
    }

    tryConnectToChatSocket() {
        if (!this.chatSocket) {
            try {
                this.chatSocket = new WebSocket(
                    'ws://'
                    + window.location.host
                    + '/ws/chat/'
                );
                this.loadEventHandlers()
                this.handleMessage = this.handleMessage.bind(this);
                console.log("socket connected");
            } catch(err) {
                this.chatSocket = null;
                console.log("Couldn't connect to chat websocket, will try again latter.");
            }
        }
        return;
    }

    disconnectChatSocket() {
        if (this.chatSocket) {
            this.chatSocket.close();
            this.chatSocket = undefined;
        }
        console.log("close socket");
        return;
    }

    loadEventHandlers() {
        console.log('Loading chat manager event handlers...');
        this.chatSocket.addEventListener("message", this.handleMessage);
    }

    handleMessage(event) {
        console.log("handleMessage() called");
        try {
            var data = JSON.parse(event.data);
            let messageInfo = {
                ...data,
                'time': Date.now()
            }
            this.atualizaHistorico(messageInfo);
            document.dispatchEvent(new CustomEvent('chatMessageReceived', {detail: messageInfo.chat_id}));
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