import Profile from "./views/profile.js";
import Play from "./views/play.js";
import EnterOnline from "./views/enter_online.js";
import EnterTournament from "./views/enter_tournament.js";
import Chat from "./views/chat.js";
import Friends from "./views/friends.js";
import ChatManager from "./managers/ChatManager.js";
import Change_password from "./views/change_password.js";
import friendshipFormsHandler from "./handlers/friendshipFormsHandler.js";
import userBlockFormsHandler from "./handlers/userBlockFormsHandler.js";
import localGameFormsHandler from "./handlers/localGameFormHandler.js";
import Room from "./views/roomView.js";

var view = null;

var chatManager = new ChatManager();

chatManager.loadEventHandlers();

export const navigateTo = (url) => {
    //tratamento de url relativa para absoluta
    history.pushState(null, null, url);
    viewsRouter(url);
};

const viewsRouter = async (url) => {
    const routes = [
        { path: "/profile/", view: Profile },
        { path: "/play/", view: Play },
        { path: "/enter/online/", view: EnterOnline },
        { path: "/enter/tournament/", view: EnterTournament },
        { path: "/chat/", view: Chat },
        { path: "/friends/", view: Friends },
        { path: "/change_password/", view: Change_password },
        { path: "/room/:id/", view: Room, regex: /^\/room\/\d+\/$/ },
    ];

    const potentialMatches = routes.map(route => {
        const isMatch = route.regex
            ? route.regex.test(location.pathname) // Use regex for dynamic routes
            : location.pathname === route.path;

        return {
            route: route,
            isMatch: isMatch,
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
    document.querySelector("#app").innerHTML = await view.getHtml(url);
    await view.loadComponents();
    view.bindUIEventHandlers();

};

const handlersRouter = async (form) => {
    const routes = [
        { formType: "friendshipForm", handler: friendshipFormsHandler },
        { formType: "blockForm", handler: userBlockFormsHandler },
        { formType: "localGameForm", handler: localGameFormsHandler },
    ];

    let match = routes.find((route) => form.getAttribute('formType') === route.formType);

    if (!match) {
        return;
    }

    const handler = new match.handler();
    const jsonResponse = await handler.postForm(form);
    const context = handler.getContext(form, jsonResponse);
    await handler.updateUI(view, context);
};

window.addEventListener("popstate", viewsRouter);

function submitForm(form) {
    handlersRouter(form);
}

document.addEventListener("DOMContentLoaded", () => {

    console.log("Página carregada, chamando routers()");
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
