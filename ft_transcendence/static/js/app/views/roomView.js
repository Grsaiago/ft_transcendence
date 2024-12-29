import AbstractView from "./abstractView.js";
import PongRoomManager from "../managers/PongRoomManager.js";

export default class Room extends AbstractView {
    constructor() {
        super();
        this.setTitle("Play");
        this.pongRoomManager = new PongRoomManager();
    }

    async getHtml(url) {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('Play html fetched. Returning...');
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading login page</p>";
        }
    }

    loadComponents() {
        this.initGame();
    }

    bindUIEventHandlers() {
        this.bindMovementHandlers();
        this.bindStartButtonHandler();
        this.bindPongRoomEventHandlers()
    }

    removeUIEventHandlers() {
        this.unbindMovementHandler();
        this.unbindStartButtonHandler();
        this.unbindPongRoomEventHandlers();
    }

    //Creating game canvas and connecting to socket

    initGame()
    {
        this.loadGameData();

        this.pongRoomManager.createGame();

        this.pongRoomManager.connectSocket();

        this.pongRoomManager.loadSocketEventHandlers();
    }

    loadGameData() {
        //Get canvas and context
        const canvas = document.getElementById("pongCanvas");
        const context = canvas.getContext("2d");
    
        //Get game info
        const gameData = document.getElementById("game-data");
        const roomId = gameData.dataset.roomId;
        const gameMode = gameData.dataset.gameMode;

        this.pongRoomManager.setGameData(context, canvas.width, canvas.height, roomId, gameMode);
    }

    //Key events Handlers

    handleKeyEvent(event, keyType) {
        const validKeys = ["ArrowUp", "ArrowDown", "w", "s", "W", "S"];
        if (validKeys.includes(event.key)) {
          event.preventDefault();
          const message = {
            type: keyType,
            key: event.key.toLocaleLowerCase(),
          };
          this.pongRoomManager.sendMessage(message);
        }
    }

    handleClickStartButton() {
        const message = {
          type: "start_game",
        };
        this.pongRoomManager.sendMessage(message);
    }

    //PongRoom Events Handlers

    handleGameHasStarted() {
        console.log("GameStarted received")
        startButton = document.getElementById("startGame");
        startButton.style.display = "none";
        const messageContainer = document.getElementById("messageContainer");
        messageContainer.textContent = "Game has started!";
        log.info("Game has started!");
    }

    handleWinner(event) {
        console.log("Winner received")
        const messageContainer = document.getElementById("messageContainer");
        messageContainer.textContent = `${event.player_winner} wins!`;
        startButton = document.getElementById("startGame");
        startButton.textContent = "Play Again!";
        startButton.style.display = "block";
    }

    handleRedirectTournament(redirect) {
        window.location.href = redirect; //navigateTo
    }

    //Binders
    bindPongRoomEventHandlers() {
        document.addEventListener('GameStarted', this.handleGameHasStarted);
        document.addEventListener('Winner', this.handleWinner);
        document.addEventListener('RedirectTournament', this.handleRedirectTournament);
    }

    bindMovementHandlers() {
        document.addEventListener("keydown", (event) => {
            this.handleKeyEvent(event, "keydown");
        });
        
            document.addEventListener("keyup", (event) => {
            this.handleKeyEvent(event, "keyup");
        });
    }

    bindStartButtonHandler() {
        const startButton = document.getElementById("startGame");
        startButton.addEventListener("click", () => {
            this.handleClickStartButton();
        });
    }

    //Unbinders
    unbindMovementHandler() {
        document.removeEventListener("keydown", (event) => {
            this.handleKeyEvent(event, "keydown");
        });
        
        document.removeEventListener("keyup", (event) => {
            this.handleKeyEvent(event, "keyup");
        });
    }

    unbindStartButtonHandler() {
        const startButton = document.getElementById("startGame");
        startButton.removeEventListener("click", () => {
            this.handleClickStartButton();
        });
    }

    unbindPongRoomEventHandlers() {
        document.removeEventListener('GameStarted', this.handleGameHasStarted);
        document.removeEventListener('Winner', this.handleWinner);
        document.removeEventListener('RedirectTournament', this.handleRedirectTournament);
    }
}