import Profile from "./views/profile.js";
import Play from "./views/play.js";
import Chat from "./views/chat.js";
import ChatManager from "./managers/ChatManager.js";
import Change_password from "./views/change_password.js";

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
        {path: "/play/", view: Play },
        {path: "/chat/", view: Chat },
        {path: "/change_password/", view: Change_password },
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

    });

    router();
});