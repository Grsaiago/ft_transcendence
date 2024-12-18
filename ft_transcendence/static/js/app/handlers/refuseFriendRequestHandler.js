import AbstractHandler from "./abstractHandler.js";

export default class RefuseFriendRequestHandler extends AbstractHandler {
    constructor() {
        super();
    }

    updateUI() {
        alert("Friend request refused.");
    }
}