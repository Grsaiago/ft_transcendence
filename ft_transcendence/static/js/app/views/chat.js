
import AbstractView from "./abstractView.js";

export default class Chat extends AbstractView {
    constructor() {
        super();
        this.setTitle("Chat");
    }

    async getHtml() {
        try {
            const response = await fetch('/chat/', {
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
}
