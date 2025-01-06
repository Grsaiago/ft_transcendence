import { navigateTo } from "../index.js";
import LocalTournamentManager from "../managers/localTournamentManager.js";
import AbstractView from "./abstractView.js";

export default class EnterLocalTournament extends AbstractView {
    constructor() {
        super();
        this.setTitle("Create Local Tournament");
        this.localTournamentManager = new LocalTournamentManager();
    }

    async getHtml() {
        try {
            const response = await fetch('/enter/localtournament/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('enter/tournament html fetched. Returning...');
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading enter/tournament page</p>";
        }
    }

    bindUIEventHandlers() {
        console.log('Loading enter event handlers...');
        const tournamentInput = document.getElementById("tournament-name");
        const buttons = document.querySelectorAll(".btn-custom");

        const redirectTo = (maxPlayers) => {
            const url = `/localTournament/${maxPlayers}/`;
            console.log(`Redirecting to: ${url}`);
            navigateTo(url);
        };

        buttons.forEach((button) => {
            button.addEventListener("click", (event) => {
                event.preventDefault(); // Prevent default button behavior
                const maxPlayers = button.getAttribute("value");
                const tournamentName = tournamentInput.value;

                this.localTournamentManager.name = tournamentName;
                this.localTournamentManager.num_of_players = maxPlayers;

                if (!tournamentName.trim()) {
                    alert("Please enter a tournament name!");
                    return;
                }

                redirectTo(maxPlayers);
            });
        });
    }

    removeUIEventHandlers() {
        console.log('Removing enter event handlers...');
        const buttons = document.querySelectorAll(".btn-custom");
        buttons.forEach((button) => {
            const newButton = button.cloneNode(true);
            button.parentNode.replaceChild(newButton, button);
        });
    }
}
