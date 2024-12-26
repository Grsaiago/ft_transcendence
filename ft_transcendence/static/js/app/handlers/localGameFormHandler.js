import AbstractHandler from "./abstractHandler.js";
export default class localGameFormsHandler extends AbstractHandler {
    constructor() {
        super();
        this.updateUI = this.updateUI.bind(this);
    }

    async updateUI(view, context) {
        console.log(`Load /room/${context}`);
    }

    getContext(_form) {
        return null
    }
}
