import AbstractView from "./abstractView.js";
import ChatManager from "../managers/ChatManager.js";

export default class EnterOnline extends AbstractView {
    constructor() {
        super();
        // tenta conectar o socket de chat
        const chatManager = new ChatManager();
        chatManager.tryConnectToChatSocket();
        this.setTitle("EnterOnline");
    }

    async getHtml() {
        try {
            const response = await fetch('/enter/online/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('enter/online html fetched. Returning...');
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading enter/online page</p>";
        }
    }

    bindUIEventHandlers() {
        console.log('Loading enter event handlers...');
    }

    removeUIEventHandlers() {
        console.log('Removing enter event handlers...');
    }
}
