import AbstractHandler from "./abstractHandler.js";

export default class profileFormsHandler extends AbstractHandler {
    constructor() {
        super();
        this.updateUI = this.updateUI.bind(this);
    }

    async updateUI(view, id) {
        view.bindUIEventHandlers();
        console.log("updateUI called")
    }
}