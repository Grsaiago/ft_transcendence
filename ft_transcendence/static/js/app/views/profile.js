import AbstractView from "./abstractView.js";

export default class Profile extends AbstractView {
    constructor() {
        super();
        this.setTitle("Profile");
    }

    async getHtml() {
        try {
            const response = await fetch('/profile/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('Profile html fetched. Returning...');
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading login page</p>";
        }
    }

    bindUIEventHandlers() {
        console.log('Loading profile event handlers...');
    }

    removeUIEventHandlers() {
        console.log('Removing profile event handlers...');
    }
}
