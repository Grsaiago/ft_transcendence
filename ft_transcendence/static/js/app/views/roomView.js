import AbstractView from "./abstractView.js";

export default class Room extends AbstractView {
    constructor() {
        super();
        this.setTitle("Room");
    }

    async getHtml(url) {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('Room html fetched. Returning...');
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading Room page</p>";
        }
    }

    async loadComponents() {
        console.log('Loading Room components...');
        // Carregando o script handle-Room.js dinamicamente
        await import('../pong/handle-pong.js').then((module) => {
            console.log("Room script loaded successfully");
        }).catch((error) => {
            console.error("Failed to load Room script: ", error);
        });
    }

    bindUIEventHandlers() {
        console.log('Loading Room event handlers...');
    }

    removeUIEventHandlers() {
        console.log('Removing Room event handlers...');
    }
}