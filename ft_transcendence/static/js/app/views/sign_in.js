import AbstractView from "./abstractView.js";

export default class Sign_in extends AbstractView {
    constructor() {
        super();
        this.setTitle("Sign_in");
    }

    async getHtml() {
        try {
            const response = await fetch('/sign_in/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading login page</p>";
        }
    }

    bindUIEventHandlers() {
        console.log('Loading login event handlers...');
    }

    removeUIEventHandlers() {
        console.log('Removing login event handlers...');
    }
}
