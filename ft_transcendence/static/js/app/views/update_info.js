
import AbstractView from "./abstractView.js";

export default class Update_info extends AbstractView {
    constructor() {
        super();
        this.setTitle("Update_info");
    }

    async getHtml() {
        try {
            const response = await fetch('/update_info/', {
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
        console.log('Loading update info event handlers...');
    }

    removeUIEventHandlers() {
        console.log('Removing update info event handlers...');
    }
}
