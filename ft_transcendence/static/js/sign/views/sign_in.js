import AbstractView from "./abstractView.js";

export default class Sign_in extends AbstractView {
    constructor() {
        super();
        this.setTitle("Sign_in");
    }

    async getHtml() {
        try {
            const response = await fetch('/login/', {
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
