import AbstractView from "./abstractView.js";

export default class EnterTournament extends AbstractView {
    constructor() {
        super();
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
