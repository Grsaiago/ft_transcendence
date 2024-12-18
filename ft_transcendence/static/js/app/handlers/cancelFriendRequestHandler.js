import AbstractHandler from "./abstractHandler.js";

export default class CancelFriendRequestHandler extends AbstractHandler {
    constructor() {
        super();
    }

    updateUI() {
        alert('Friend request refused.');
    }
}