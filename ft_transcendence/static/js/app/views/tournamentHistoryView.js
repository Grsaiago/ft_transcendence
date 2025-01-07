import AbstractView from "./abstractView.js";

export default class TournamentHistoryView extends AbstractView {
    constructor() {
        super();
        this.setTitle("Tournament History");
    }

    async getHtml(url) {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('TournamentHistory html fetched. Returning...');
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading login page</p>";
        }
    }

    bindUIEventHandlers() {
        console.log('Loading TournamentHistory event handlers...');
    }

    removeUIEventHandlers() {
        console.log('Removing TournamentHistory event handlers...');
    }
}
