import AbstractView from "./abstractView.js";
import ChatManager from "../managers/ChatManager.js";

export default class Change_password extends AbstractView {
    constructor() {
        super();
        // tenta conectar o socket de chat
        const chatManager = new ChatManager();
        chatManager.tryConnectToChatSocket();
        this.setTitle("Change_password");
    }

    async getHtml() {
        try {
            const response = await fetch('/change_password/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log(html);
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading login page</p>";
        }
    }

    bindUIEventHandlers() {
        console.log('Loading Change password event handlers...');
    }

    removeUIEventHandlers() {
        console.log('Removing Change password event handlers...');
    }
}
