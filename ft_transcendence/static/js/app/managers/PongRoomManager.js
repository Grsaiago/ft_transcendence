export default class PongRoomManager {
    constructor () {

        this.handleSocketOpen = this.handleSocketOpen.bind(this);
        this.handleSocketMessage = this.handleSocketMessage.bind(this);
    }

    connectSocket(socketUrl)
    {
        this.socket = new WebSocket(socketUrl);
    }

    createGame(context, width, height)
    {
        //Initialize game
        this.pongGame = new PongGame(context, width, height);
    }

    loadEventHandlers() {
        this.socket.onopen = (event) => {
            this.handleSocketOpen(event);
        };
        
        this.socket.onmessage = (event) => {
            this.handleSocketMessage(event);
        };
        
        this.socket.onclose = (event) => {
            log.info("WebSocket connection closed", event.code);
        };
        
        this.socket.onerror = (event) => {
            log.error("WebSocket connection error", event);
        };
    }

    handleSocketOpen(event) {
        const message = {
            type: "join_room",
            room_id: roomId,
            width: canvas.width,
            height: canvas.height,
        };
        this.sendMessage(message);
        log.info("WebSocket connection established with:", event);
    }
      
    handleSocketMessage(event) {
        const data = JSON.parse(event.data);
        log.info("Message from server:", data);
        
        switch (data.type) {
            case "not_auth":
            alert(data.message);
            socket.close();
            break;
        
            case "game_init":
            pongGame.drawGameState(data.game_state);
            break;
        
            case "update_game_state":
            pongGame.drawGameState(data.game_state);
            break;
        
            case "game_has_started":
            this.handleGameHasStarted();
            break;
        
            case "winner":
            handleWinner(data.winner);
            break;
        
            case "redirect_tournament":
            handleRedirectTournament(data.redirect);
            break
        
            default:
            log.error("Unknown message type:", data.type);
        }
    }

    handleGameHasStarted() {
        startButton.style.display = "none";
        const messageContainer = document.getElementById("messageContainer");
        messageContainer.textContent = "Game has started!";
        log.info("Game has started!");
    }

    handleWinner(winner) {
        const messageContainer = document.getElementById("messageContainer");
        messageContainer.textContent = `${winner} wins!`;
        startButton.textContent = "Play Again!";
        startButton.style.display = "block";
      }

    sendMessage(message) {
        const jsonMessage = JSON.stringify(message);
        log.debug("Sending message:", jsonMessage);
        this.socket.send(jsonMessage);
    }
}