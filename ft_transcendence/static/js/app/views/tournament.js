import AbstractView from "./abstractView.js";

export default class Tournament extends AbstractView {
    constructor() {
        super();
        this.setTitle("Tournament");
        this.joinButton = null;
        this.username = null;
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
        console.log('Loading Tournament components...');
    }

    bindUIEventHandlers() {
        console.log('Loading play event handlers...');

        this.initTournamentPage();

        this.joinButton = document.getElementById("joinTournament");
        
        this.joinButton.addEventListener("click", () => {
            this.handleClickJoinButton();
        });
    }

    removeUIEventHandlers() {
        console.log('Removing play event handlers...');
    
        this.joinButton.removeEventListener("click", () => {
            this.handleClickJoinButton(socket, this.joinButton);
        });
    }

    initTournamentPage() {
        const hostname = window.location.hostname;
        if (hostname === "www.transcendence.com") {
            log.setLevel(log.levels.ERROR);
        } else {
            log.setLevel(log.levels.DEBUG);
        }

        const gameData = document.getElementById("game-data");
        this.username = gameData.dataset.username;
        const tournamentId = gameData.dataset.tournamentId;
        const gameMode = gameData.dataset.gameMode;

        log.info("tournament_id:", tournamentId);
        log.info("game_mode:", gameMode);

        if (gameMode !== "tournament") {
            log.error("Invalid game mode");
        }

        //Websocket connection
        const socketUrl = `ws://${window.location.host}/ws/pong/tournament/${tournamentId}/`;
        const socket = new WebSocket(socketUrl);

        //Websocket
        socket.onopen = (event) => {
            log.info("WebSocket connection opened", event);
        };

        socket.onmessage = (event) => {
            this.handleSocketMessage(event);
        };

        socket.onclose = (event) => {
            log.info("WebSocket connection closed", event.code);
        };

        socket.onerror = (event) => {
            log.error("WebSocket connection error", event);
        };
    }

    handleSocketMessage(event) {
        const data = JSON.parse(event.data);
        log.info("handleSocketMessage:", data);
      
        switch (data.type) {
            case "not_auth":
                alert(data.message);
                socket.close();
                break;
            case "joined":
                this.joinButton.classList.add("disabled");
                this.joinButton.disabled = true;
                break;
            case "current_state":
                this.handleCurrentState(data);
                break;
      
            case "tournament_message":
                this.handleTournamentMessage(data);
                break;
        
            case "tournament_advance":
                this.handleTournamentAdvance(data);
                break;
        
            case "error":
                this.handleErrorMessage(data);
                break;
        
            default:
                log.error("Invalid message type:", data.type);
        }
    }
      
    handleCurrentState(data) {
        log.info("handleCurrentState:", data);
        this.updateTournamentUI(data.state);
    }

    handleTournamentMessage(data) {
        log.info("handleTournamentMessage:", data);
        this.displayTournamentMessage(data.message);
    }

    handleTournamentAdvance(data) {
        log.info("tournament_advance:", data);
        this.updateTournamentUI(data.state);
    }

    handleErrorMessage(data) {
        log.info("error:", data);
        this.displayErrorMessage(data.message);
    }

    handleClickJoinButton() {
        sendMessage({
            type: "join_tournament"
        });
    }

    sendMessage(message) {
        const jsonMessage = JSON.stringify(message);
        log.debug("Sending message:", jsonMessage);
        socket.send(jsonMessage);
    }

    updateTournamentUI(state) {
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
            const buttonElem = document.getElementById(`${match.round}-btn`);
            log.info("player1Elem:", player1Elem);
            log.info("player2Elem:", player2Elem);
            log.info("buttonElem:", buttonElem);

            if (player1Elem)
                player1Elem.innerText = match.player1 !== "TBD" ? match.player1 : "TBD";
            if (player2Elem)
                player2Elem.innerText = match.player2 !== "TBD" ? match.player2 : "TBD";

            if (buttonElem) {
                if (
                    (match.player1 === this.username || match.player2 === this.username) &&
                    !match.finished &&
                    match.player1 !== "TBD" &&
                    match.player2 !== "TBD"
                ) {
                    buttonElem.style.display = "block";
                    buttonElem.onclick = () => this.redirectToMatch(match.room_id);
                } else {
                    buttonElem.classList.add("disabled");
                    // buttonElem.style.display = "none";
                }
            }
        });
    }

    // Função para redirecionar para a partida
    redirectToMatch(roomId) {
        window.location.href = `/room/${roomId}/`;
    }

    //function to display tournament message
    displayTournamentMessage(message) {
        const tournamentStatusMsg = document.getElementById("tournamentMessages");
        if (tournamentStatusMsg) {
          tournamentStatusMsg.innerText = message;
        }
    }

    //function to display error message
    displayErrorMessage(message) {
        const tournamentErrorMsg = document.getElementById("tournamentErrorMsg");
        if (tournamentErrorMsg) {
          tournamentErrorMsg.innerText = message;
        }
    }

}