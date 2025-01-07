import AbstractView from "./abstractView.js";

export default class MatchHistoryView extends AbstractView {
    constructor() {
        super();
        this.setTitle("Match History");
    }

    async getHtml(url) {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('MatchHistory html fetched. Returning...');
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading login page</p>";
        }
    }

    bindUIEventHandlers() {
        console.log('Loading MatchHistory event handlers...');
    }

    removeUIEventHandlers() {
        console.log('Removing MatchHistory event handlers...');
    }
}
