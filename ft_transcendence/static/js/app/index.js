import Profile from "./views/profile.js";
import Play from "./views/play.js";
import EnterOnline from "./views/enter_online.js";
import EnterTournament from "./views/enter_tournament.js";
import Chat from "./views/chat.js";
import Friends from "./views/friends.js";
import WebSocketManager from "./managers/WebSocketManager.js";
import Change_password from "./views/change_password.js";
import Update_info from "./views/update_info.js";
import friendshipFormsHandler from "./handlers/friendshipFormsHandler.js";
import userBlockFormsHandler from "./handlers/userBlockFormsHandler.js";
import UpdateInfoFormsHandler from "./handlers/updateInfoFormHandler.js";
import ChangePasswordFormsHandler from "./handlers/changePasswordFormHandler.js";
import localGameFormsHandler from "./handlers/localGameFormHandler.js";
import Room from "./views/roomView.js";
import WebSocketManager from "./managers/WebSocketManager.js";

var view = null;

var wSManager = new WebSocketManager();

wSManager.chatManager.loadEventHandlers();

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
        {path: "/update_info/", view: Update_info },
        { path: "/room/:id/", view: Room, regex: /^\/room\/\d+\/$/ },
    ];

    let match = routes.find((route) =>  route.regex
        ? route.regex.test(location.pathname) // Use regex for dynamic routes
        : location.pathname === route.path);

    if (!match) {
        match = {
            route: routes[0],
            isMatch: true
        };
    }

    if (view) {
        view.removeUIEventHandlers();
    }

    view = new match.view();
    document.querySelector("#app").innerHTML = await view.getHtml(url);
    await view.loadComponents();
    view.bindUIEventHandlers();

};

const handlersRouter = async (form) => {
    const routes = [
        { formType: "friendshipForm", handler: friendshipFormsHandler },
        { formType: "blockForm", handler: userBlockFormsHandler },
        { formType: "localGameForm", handler: localGameFormsHandler },
        { formType: "updateInfoForm", handler: UpdateInfoFormsHandler},
        { formType: "changePasswordForm", handler: ChangePasswordFormsHandler},
    ];

    let match = routes.find((route) => form.getAttribute('formType') === route.formType);

    if (!match) {
        return;
    }

    const handler = new match.handler();
    const Response = await handler.postForm(form);
    const context = handler.getContext(form, Response);
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
