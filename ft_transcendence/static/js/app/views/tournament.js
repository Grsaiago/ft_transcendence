import AbstractView from "./abstractView.js";
import ChatManager from "../managers/ChatManager.js";

export default class Tournament extends AbstractView {
    constructor() {
        super();
        // tenta conectar o socket de chat
        const chatManager = new ChatManager();
        chatManager.tryConnectToChatSocket();
        this.setTitle("Tournament");
    }

    async getHtml(url) {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('Tournament html fetched. Returning...');
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading Tournament page</p>";
        }
    }

    async loadComponents() {
        console.log('Loading Tournament components...');
        // Carregando o script handle-tournament.js dinamicamente
        await import('../pong/handle-tournament.js').then((module) => {
            console.log("Tournament script loaded successfully");
        }).catch((error) => {
            console.error("Failed to load tournament script: ", error);
        });
    }

    bindUIEventHandlers() {
        console.log('Loading Tournament event handlers...');
    }

    removeUIEventHandlers() {
        console.log('Removing Tournament event handlers...');
    }
}