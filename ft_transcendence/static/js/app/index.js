import Profile from "./views/profile.js";
import Chat from "./views/chat.js";
import Friends from "./views/friends.js";
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
        {path: "/chat/", view: Chat },
        {path: "/friends/", view: Friends },
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

    
    document.body.addEventListener("submit", e => {
        const form = e.target;
        const allowedFormIds = ["accept-friend-request", "refuse-friend-request", "cancel-friend-request"];
        const friendsView = new Friends();        
        
        if (form.tagName === "FORM" && allowedFormIds.includes(form.id)) {
            e.preventDefault();
            console.log(e.target);
            
            const formData = new FormData(form);
            const data = new URLSearchParams(formData);
            
            fetch(form.action, {
                method: form.method,
                body: data,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
                .then(response => {
                    if (response.ok) {
                        console.log("Success:", data);
                        navigateTo("/friends/");
                        friendsView.toggleTabs("search"); //nao esta funcionando. tem que refatorar a classe friends depois!
                    } else {
                        console.error("Failed to submit form:", response.statusText);
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                });
            }
        });
        
        router();

});