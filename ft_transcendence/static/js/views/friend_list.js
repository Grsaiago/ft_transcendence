import AbstractView from "./abstractView.js";

export default class FriendList extends AbstractView {
    constructor() {
        super();
        this.setTitle("Friend List");
    }

    async getHtml() {
        try {
            const response = await fetch('/friend_list/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading frient_list page</p>";
        }
    }
}