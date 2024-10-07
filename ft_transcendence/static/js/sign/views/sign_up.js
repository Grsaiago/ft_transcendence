import AbstractView from "./abstractView.js";

export default class Sign_up extends AbstractView {
    constructor() {
        super();
        this.setTitle("Sign_up");
    }

    async getHtml() {
        try {
            const response = await fetch('/register/', {
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
            return "<p>Error loading register page</p>";
        }
    }
}
