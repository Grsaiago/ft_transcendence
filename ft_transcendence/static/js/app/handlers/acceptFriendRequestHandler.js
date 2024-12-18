import AbstractHandler from "./abstractHandler.js";

export default class AcceptFriendRequestHandler extends AbstractHandler {
    constructor() {
        super();
    }

    updateUI() {
        alert("Friend request accepted.");
    }
}