import AbstractView from "./abstractView.js";

export default class Play extends AbstractView {
    constructor() {
        super();
        this.setTitle("Play");
    }

    async getHtml() {
        try {
            const response = await fetch('/play/', {
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

    bindUIEventHandlers() {
        console.log('Loading play event handlers...');
    }

    removeUIEventHandlers() {
        console.log('Removing play event handlers...');
    }
}
