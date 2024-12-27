import AbstractHandler from "./abstractHandler.js";

export default class userBlockFormsHandler extends AbstractHandler {
    constructor() {
        super();
        this.updateUI = this.updateUI.bind(this);
    }

    async updateUI(view, id, response) {
        await view.loadUserDetail(id);
    }
}