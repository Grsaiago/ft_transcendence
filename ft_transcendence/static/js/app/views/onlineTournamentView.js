import HubManager from "../managers/HubManager.js";
import AbstractView from "./abstractView.js";

export default class OnlineTournament extends AbstractView {
    constructor() {
        super();
        this.setTitle("Tournament");
        this.hubManager = new HubManager();

        this.handleClickJoinButton = this.handleClickJoinButton.bind(this);
        this.handleJoinedTournament = this.handleJoinedTournament.bind(this);
        this.handleCurrentState = this.handleCurrentState.bind(this);
        this.handleTournamentMessage = this.handleTournamentMessage.bind(this);
        this.handleTournamentAdvance = this.handleTournamentAdvance.bind(this);
    }

    async getHtml(url) {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('Tournament html fetched. Returning...');
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading Tournament page</p>";
        }
    }

    async loadComponents() {
        this.initTournamentHub();
    }

    unloadComponents() {
        this.hubManager.socket.close();
    }

    initTournamentHub() {
        this.loadTournamentHubData();

        this.hubManager.connectSocket();

        this.hubManager.loadSocketEventHandlers();
    }

    loadTournamentHubData() {
        const gameData = document.getElementById("game-data");
        const tournamentId = gameData.dataset.tournamentId;
        const gameMode = gameData.dataset.gameMode;
        const username = gameData.dataset.username;

        this.hubManager.setTournamentHubData(tournamentId, gameMode, username);
    }

    bindUIEventHandlers() {
        this.bindJoinButtonHandler();
        this.bindHubManagerEventHandlers();
    }

    removeUIEventHandlers() {
        //unbind
    }

    //Button Handlers

    handleClickJoinButton() {
        this.hubManager.joinTournament();
    }

    //HubManager Events Handlers

    handleJoinedTournament() {
        const joinButton = document.getElementById("joinTournament");
        joinButton.style.display = "none";
        console.log("inscrito")
    }

    handleTournamentMessage(event) {
        log.info("handleTournamentMessage:", event.detail);
        this.displayTournamentMessage(event.detail.message);
    }

    displayTournamentMessage(message) {
        const tournamentStatusMsg = document.getElementById("tournamentMessages");
        if (tournamentStatusMsg) {
          tournamentStatusMsg.innerText = message;
        }
    }

    handleCurrentState(event) {
        this.updateTournamentUI(event.detail.state);
    }

    handleTournamentAdvance(event) {
        log.info("tournament_advance:", data);
        this.updateTournamentUI(event.detail.state);
    }

    updateTournamentUI(state) {
        //update status and winner
        const tournamentStatus = document.getElementById("statusParagraph");
        const tournamentWinner = document.getElementById("winnerParagraph");
        if (tournamentStatus)
            tournamentStatus.innerText = `Status: ${state.status}`;
        if (tournamentWinner)
            tournamentWinner.innerText = `Winner: ${state.winner}`;

        // Update participant slots
        state.participants.forEach((participant, index) => {
          const participantElem = document.getElementById(`participant-${index}`);
          if (participantElem) {
            participantElem.innerText = participant || `Player ${index + 1}`;
          }
        });

        // Update match brackets
        state.matches.forEach((match) => {
          const player1Elem = document.getElementById(`${match.round}-p1`);
          const player2Elem = document.getElementById(`${match.round}-p2`);
          const playLinkElem = document.getElementById(`${match.round}-btn`);
          log.info("player1Elem:", player1Elem);
          log.info("player2Elem:", player2Elem);
          log.info("playLinkElem:", playLinkElem);

          if (player1Elem)
            player1Elem.innerText = match.player1 !== "TBD" ? match.player1 : "TBD";
          if (player2Elem)
            player2Elem.innerText = match.player2 !== "TBD" ? match.player2 : "TBD";

          if (playLinkElem) {
            if (
              (match.player1 === this.hubManager.gameData.username || match.player2 === this.hubManager.gameData.username) &&
              !match.finished &&
              match.player1 !== "TBD" &&
              match.player2 !== "TBD"
            ) {
              playLinkElem.style.display = "block";
              playLinkElem.setAttribute('href', `/room/${match.room_id}/`);
            } else {
              playLinkElem.style.display = "none";
            }
          }
        });
    }

    //Binders

    bindJoinButtonHandler() {
        const joinButton = document.getElementById("joinTournament");
        joinButton.addEventListener("click", this.handleClickJoinButton);
    }

    bindHubManagerEventHandlers() {
        document.addEventListener('joinedTournament', this.handleJoinedTournament);
        document.addEventListener('currentState', this.handleCurrentState);
        document.addEventListener('tournamentMessage', this.handleTournamentMessage);
        document.addEventListener('tournamentAdvance', this.handleTournamentAdvance);
    }

}