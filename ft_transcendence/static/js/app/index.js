import Profile from "./views/profile.js";
import Chat from "./views/chat.js";
import Friends from "./views/friends.js";
import ChatManager from "./managers/ChatManager.js";
import Change_password from "./views/change_password.js";
import AcceptFriendRequestHandler from "./handlers/acceptFriendRequestHandler.js";
import RefuseFriendRequestHandler from "./handlers/refuseFriendRequestHandler.js";
import CancelFriendRequestHandler from "./handlers/cancelFriendRequestHandler.js";

var view = null;

var chatManager = new ChatManager();

chatManager.loadEventHandlers();

const navigateTo = url => {
    history.pushState(null, null, url);
    viewsRouter();
};

const viewsRouter = async () => {
    const routes = [
        {path: "/profile/", view: Profile },
        {path: "/chat/", view: Chat },
        {path: "/friends/", view: Friends },
        {path: "/change_password/", view: Change_password },
    ];

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

const handlersRouter = async (form) => {
    const routes = [
        {formId: "accept-friend-request", handler: AcceptFriendRequestHandler },
        {formId: "refuse-friend-request", handler: RefuseFriendRequestHandler },
        {formId: "cancel-friend-request", handler: CancelFriendRequestHandler },
    ];

    const potentialMatches = routes.map(route => {
        return {
            route: route,
            isMatch: form.id === route.formId,
        };
    });

    let match = potentialMatches.find(potentialMatch => potentialMatch.isMatch);

    if (!match) {
        return ;
    }
    
    var handler = new match.route.handler();
    handler.postForm(form);
    handler.updateUI();
    
};

window.addEventListener("popstate", viewsRouter);

function submitForm(form) {
    handlersRouter(form);
}


document.addEventListener("DOMContentLoaded", () => {
    
    console.log("Página carregada, chamando router()");
    document.body.addEventListener("click", e => {
        if (e.target.matches("[data-link]")) {
            e.preventDefault();
            navigateTo(e.target.href);
        }

    });
    
    document.body.addEventListener("submit", e => {
        const form = e.target;
        
        if (form.tagName === "FORM" && form.matches("[api-link]")) {
            console.log(e.target);
            e.preventDefault();
            submitForm(form);
        }
    });

    viewsRouter();

});