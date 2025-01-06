import AbstractView from "./abstractView.js";
import ChatManager from "../managers/ChatManager.js";

export default class EnterTournament extends AbstractView {
    constructor() {
        super();
        // tenta conectar o socket de chat
        const chatManager = new ChatManager();
        chatManager.tryConnectToChatSocket();
        this.setTitle("EnterTournament");
    }

    async getHtml() {
        try {
            const response = await fetch('/enter/tournament/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('enter/tournament html fetched. Returning...');
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading enter/tournament page</p>";
        }
    }

    bindUIEventHandlers() {
        console.log('Loading enter event handlers...');
    }

    removeUIEventHandlers() {
        console.log('Removing enter event handlers...');
    }
}
