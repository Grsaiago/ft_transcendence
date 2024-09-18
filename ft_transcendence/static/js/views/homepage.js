import AbstractView from "./abstractView.js";

export default class Homepage extends AbstractView {
    constructor() {
        super();
        this.setTitle("Homepage");
    }

    async getHtml() {
        return "<h2>Welcome to transcendence!</h2>";
    }
}
