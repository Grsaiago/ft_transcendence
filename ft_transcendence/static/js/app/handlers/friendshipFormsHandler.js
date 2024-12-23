import AbstractHandler from "./abstractHandler.js";

export default class friendshipFormsHandler extends AbstractHandler {
    constructor() {
        super();
        this.updateUI = this.updateUI.bind(this);
    }

    async updateUI(view, id) {
        //unbinding UI event handlers - NEED TO DO
        await view.loadComponents();
        //binding UI event handlers
        view.bindUIEventHandlers();
        await view.loadUserDetail(id);
    }
}