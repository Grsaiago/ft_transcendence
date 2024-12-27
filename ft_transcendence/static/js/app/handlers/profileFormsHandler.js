import AbstractHandler from "./abstractHandler.js";
import { navigateTo } from "../index.js";

export default class profileFormsHandler extends AbstractHandler {
    constructor() {
        super();
        this.updateUI = this.updateUI.bind(this);
    }

    async updateUI(view, id, response) {
        view.bindUIEventHandlers();
        if (response.ok)
            navigateTo("/profile/");
        else
            navigateTo("/change_password/");
    }
}