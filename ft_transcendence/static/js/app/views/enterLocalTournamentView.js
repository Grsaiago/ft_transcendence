import { navigateTo } from "../index.js";
import LocalTournamentManager from "../managers/localTournamentManager.js";
import AbstractView from "./abstractView.js";

export default class EnterLocalTournament extends AbstractView {
    constructor() {
        super();
        this.setTitle("Create Local Tournament");
        this.localTournamentManager = new LocalTournamentManager();

        this.redirectTo = this.redirectTo.bind(this);
        this.handleCreateTournBtn = this.handleCreateTournBtn.bind(this);
        this.handleCreate4TournBtn = this.handleCreate4TournBtn.bind(this);
        this.handleCreate8TournBtn = this.handleCreate8TournBtn.bind(this);
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

    loadComponents() {
        if (this.localTournamentManager.status !== "Started") {
            this.hideContinueDiv();
        }
        else {
            this.loadCurrentTournamentName();
        }
    }

    loadCurrentTournamentName() {
        const nameInput = document.getElementById('continue-tournament-name');
        nameInput.value = this.localTournamentManager.name;
        nameInput.disabled = true;
    }

    hideContinueDiv() {
        document.getElementById('continue').classList.add('d-none');
    }

    bindUIEventHandlers() {
        console.log('Loading enter event handlers...');
        document.getElementById('enter-4').addEventListener('click', this.handleCreate4TournBtn);
        document.getElementById('enter-8').addEventListener('click', this.handleCreate8TournBtn);
        document.getElementById('enter-continue').addEventListener('click', this.redirectTo);
    }

    handleCreate4TournBtn = (event) => this.handleCreateTournBtn(event, 4);

    handleCreate8TournBtn = (event) => this.handleCreateTournBtn(event, 8);

    handleCreateTournBtn (event, maxPlayers) {
        event.preventDefault(); // Prevent default button behavior

        const tournamentInput = document.getElementById("tournament-name");
        const tournamentName = tournamentInput.value;

        if (!tournamentName.trim()) {
            alert("Please enter a tournament name!");
            return;
        }

        if (this.localTournamentManager.status === "Started") {
            const confirmOverwrite = confirm(
                "A tournament is already in progress. Creating a new local tournament will overwrite the current one. Do you want to continue?"
            );
            if (!confirmOverwrite) {
                return;
            }
        }
        
        this.localTournamentManager.resetTournament();

        this.localTournamentManager.name = tournamentName;
        this.localTournamentManager.num_of_players = maxPlayers;

        this.redirectTo();
    }

    redirectTo = () => {
        const maxPlayers = this.localTournamentManager.num_of_players;
        const url = `/localTournament/${maxPlayers}/`;
        console.log(`Redirecting to: ${url}`);
        navigateTo(url);
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
