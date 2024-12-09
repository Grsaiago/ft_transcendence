//Set environment
const hostname = window.location.hostname;
if (hostname === "www.transcendence.com") {
  log.setLevel(log.levels.ERROR);
} else {
  log.setLevel(log.levels.DEBUG);
}

//Get game data
const gameData = document.getElementById("game-data");
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
  handleSocketMessage(event);
}

socket.onclose = (event) => {
  log.info("WebSocket connection closed", event.code);
}

socket.onerror = (event) => {
  log.error("WebSocket connection error", event);
}

//Event listerners - Join tournament button
const joinButton = document.getElementById("joinTournament");
joinButton.addEventListener("click", () => {
  handleClickJoinButton();
});

//Functions
function handleSocketMessage(event) {
  const data = JSON.parse(event.data);
  log.info("Received message:", data);

  switch (data.type) {
    case "not_auth":
        alert(data.message);
        socket.close();
        break;

    case "current_state":
        handleCurrentState(data);
        break;

    case "tournament_update":
        handleTournamentUpdate(data);
        break;

    case "tournament_advance":
        handleTournamentAdvance(data);
        break;

    default:
        log.error("Invalid message type:", data.type);
  }
};

function handleCurrentState(data) {
    log.info ("current_state:", data);
}

function handleTournamentUpdate(data) {
    log.info("tournament_update:", data);
}

function handleTournamentAdvance(data) {
    log.info("tournament_advance:", data);
}

function sendMessage(message) {
    const jsonMessage = JSON.stringify(message);
    log.debug("Sending message:", jsonMessage);
    socket.send(jsonMessage);
  }
