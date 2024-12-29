
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
const username = gameData.dataset.username;

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
};

socket.onclose = (event) => {
  log.info("WebSocket connection closed", event.code);
};

socket.onerror = (event) => {
  log.error("WebSocket connection error", event);
};

//Event listerners - Join tournament button
const joinButton = document.getElementById("joinTournament");
joinButton.addEventListener("click", () => {
  console.log("button join tournament clicked")
  handleClickJoinButton();
});

//Functions
function handleSocketMessage(event) {
  const data = JSON.parse(event.data);
  log.info("handleSocketMessage:", data);

  switch (data.type) {
    case "not_auth":
      alert(data.message);
      socket.close();
      break;

    case "joined":
      joinButton.style.display = "none";
      break;

    case "current_state":
      handleCurrentState(data);
      break;

    case "tournament_message":
      handleTournamentMessage(data);
      break;

    case "tournament_advance":
      handleTournamentAdvance(data);
      break;

    case "error":
      handleErrorMessage(data);
      break;

    default:
      log.error("Invalid message type:", data.type);
  }
}

function handleCurrentState(data) {
  log.info("handleCurrentState:", data);
  updateTournamentUI(data.state);
}

function handleTournamentMessage(data) {
  log.info("handleTournamentMessage:", data);
  displayTournamentMessage(data.message);
}

function handleTournamentAdvance(data) {
  log.info("tournament_advance:", data);
  updateTournamentUI(data.state);
}

function handleErrorMessage(data) {
  log.info("error:", data);
  displayErrorMessage(data.message);
}

function handleClickJoinButton() {
  sendMessage({
    type: "join_tournament"
  });
  joinButton.style.display = "none";
}

function sendMessage(message) {
  const jsonMessage = JSON.stringify(message);
  log.debug("Sending message:", jsonMessage);
  socket.send(jsonMessage);
}

function updateTournamentUI(state) {
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
        (match.player1 === username || match.player2 === username) &&
        !match.finished &&
        match.player1 !== "TBD" &&
        match.player2 !== "TBD"
      ) {
        buttonElem.style.display = "block";
        buttonElem.onclick = () => redirectToMatch(match.room_id);
      } else {
        buttonElem.style.display = "none";
      }
    }
  });
}

// Função para redirecionar para a partida
function redirectToMatch(roomId) {
  window.location.href = `/room/${roomId}/`;
}

//function to display tournament message
function displayTournamentMessage(message) {
  const tournamentStatusMsg = document.getElementById("tournamentMessages");
  if (tournamentStatusMsg) {
    tournamentStatusMsg.innerText = message;
  }
}

//function to display error message
function displayErrorMessage(message) {
  const tournamentErrorMsg = document.getElementById("tournamentErrorMsg");
  if (tournamentErrorMsg) {
    tournamentErrorMsg.innerText = message;
  }
}
