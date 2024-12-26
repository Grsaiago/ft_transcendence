
import AbstractView from "./abstractView.js";

export default class Change_password extends AbstractView {
    constructor() {
        super();
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
