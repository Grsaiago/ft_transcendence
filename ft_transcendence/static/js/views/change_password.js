import AbstractView from "./abstractView.js";

export default class ChangePassword extends AbstractView {
    constructor() {
        super();
        this.setTitle("Change Password");
    }

    async getHtml() {
        return `
            <p>View of change_password.js</p>
        `;
    }
}
