import AbstractView from "./abstractView.js";

export default class Tournament extends AbstractView {
    constructor() {
        super();
        this.setTitle("Play");
    }

    async getHtml(url) {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('Play html fetched. Returning...');
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading login page</p>";
        }
    }

    async loadComponents() {
        console.log('Loading Tournament components...');
        // Carregando o script handle-tournament.js dinamicamente
        await import('./handle-tournament.js').then((module) => {
            console.log("Tournament script loaded successfully");
        }).catch((error) => {
            console.error("Failed to load tournament script: ", error);
        });
    }

    bindUIEventHandlers() {
        console.log('Loading play event handlers...');
    }

    removeUIEventHandlers() {
        console.log('Removing play event handlers...');
    }
}