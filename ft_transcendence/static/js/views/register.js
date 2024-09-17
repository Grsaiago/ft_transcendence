import AbstractView from "./abstractView.js";

export default class Register extends AbstractView {
    constructor() {
        super();
        this.setTitle("Register");
    }

    async getHtml() {
        return `
            <p>View of register.js</p>
        `;
    }
}
