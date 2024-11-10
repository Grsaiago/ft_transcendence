import Profile from "./views/profile.js";
import Chat from "./views/chat.js";
import ChatManager from "./managers/ChatManager.js";

var view = null;

var chatManager = new ChatManager();

chatManager.loadEventHandlers();

const navigateTo = url => {
    history.pushState(null, null, url);
    router();
};

const router = async () => {
    const routes = [
        {path: "/profile/", view: Profile },
        {path: "/chat/", view: Chat },
    ];

    //Test each route for potential match
    const potentialMatches = routes.map(route => {
        return {
            route: route,
            isMatch: location.pathname === route.path
        };
    });

    let match = potentialMatches.find(potentialMatch => potentialMatch.isMatch);

    if (!match) {
        match = {
            route: routes[0],
            isMatch: true
        };
    }

    if (view) {
        view.removeUIEventHandlers();
    }

    view = new match.route.view();
    document.querySelector("#app").innerHTML = await view.getHtml();
    view.bindUIEventHandlers();

};

window.addEventListener("popstate", router);

document.addEventListener("DOMContentLoaded", () => {
    console.log("Página carregada, chamando router()");

    document.body.addEventListener("click", e => {
        if (e.target.matches("[data-link]")) {
            e.preventDefault();
            navigateTo(e.target.href);
        }

        else if (e.target.matches("[data-send-msg]")) {
            console.log('Send message clicked!');

            const messageInputDom = document.getElementById('chat-message-input');
            if (!messageInputDom) {
                console.error('Message input field not found.');
                return;
            }

            const message = messageInputDom.value;

            if (!message || !view.currentChatId) {
                return;
            }

            if (chatManager.chatSocket.readyState === WebSocket.OPEN) {
                chatManager.chatSocket.send(JSON.stringify({
                    'message': message,
                    'chat_id': view.currentChatId
                }));
                messageInputDom.value = '';
            } else {
                console.log('WebSocket is not open.');
            }
        }
    });

    router();
});