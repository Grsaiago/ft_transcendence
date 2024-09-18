import AbstractView from "./abstractView.js";

export default class ChangePassword extends AbstractView {
    constructor() {
        super();
        this.setTitle("Change Password");
    }

    async getHtml() {
        try {
            const response = await fetch('/change_password/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading change_password page</p>";
        }
    }
}
