import AbstractView from "./abstractView.js";

export default class FriendList extends AbstractView {
    constructor() {
        super();
        this.setTitle("Friend List");
    }

    async getHtml() {
        return `
            <p>View of friend_list.js</p>
        `;
    }

}

