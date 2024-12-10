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
    updateTournamentUI(data);
}

function handleTournamentUpdate(data) {
    log.info("tournament_update:", data);
    displayTournamentMessage(data.message);

}

function handleTournamentAdvance(data) {
    log.info("tournament_advance:", data);
    updateTournamentUI(data.state);
}

function handleClickJoinButton() {
  sendMessage({
    type: "join_tournament",
  });
}

function sendMessage(message) {
    const jsonMessage = JSON.stringify(message);
    log.debug("Sending message:", jsonMessage);
    socket.send(jsonMessage);
  }

function updateTournamentUI(state) {
  // Atualizar elementos do DOM conforme o estado
  const maxPlayersElem = document.getElementById("maxPlayersValue");
  const statusElem = document.getElementById("statusValue");
  const participantsList = document.getElementById("participantsList");
  const matchesList = document.getElementById("matchesList");
  const tournamentStatusMsg = document.getElementById("tournamentStatusMsg");

  // Atualizar o número máximo de jogadores
  if (maxPlayersElem) {
    maxPlayersElem.innerText = state.max_players;
  }

  // Atualizar o status do torneio
  if (statusElem) {
    statusElem.innerText = state.is_active ? "Ativo" : "Finalizado";
  }

  // Atualizar a lista de participantes
  if (participantsList) {
    participantsList.innerHTML = ""; // Limpar lista anterior
    state.participants.forEach((participant) => {
      const li = document.createElement("li");
      li.innerText = participant;
      participantsList.appendChild(li);
    });
  }

  // Atualizar a lista de partidas
  if (matchesList) {
    matchesList.innerHTML = ""; // Limpar lista anterior
    state.matches.forEach((match) => {
      const li = document.createElement("li");
      li.classList.add("match-item");

      const matchInfo = `
        <strong>Match ID:</strong> ${match.id}<br>
        <strong>Player 1:</strong> ${match.player1}<br>
        <strong>Player 2:</strong> ${match.player2}<br>
        <strong>Status:</strong> ${match.finished ? "Finalizada" : "Em andamento"}<br>
        ${match.finished ? `<strong>Winner:</strong> ${match.winner}<br>` : ""}
      `;

      li.innerHTML = matchInfo;
  // Atualizar a mensagem de status do torneio
  if (tournamentStatusMsg) {
    tournamentStatusMsg.innerText = state.is_active ? "Torneio em andamento" : "Torneio finalizado";
  }

      matchesList.appendChild(li);
    });
  }
  // Atualizar a mensagem de status do torneio
  if (tournamentStatusMsg) {
    tournamentStatusMsg.innerText = state.is_active ? "Torneio em andamento" : "Torneio finalizado";
  }
}

//function to display tournament message
function displayTournamentMessage(message) {
  const tournamentStatusMsg = document.getElementById("tournamentStatusMsg");
    if (tournamentStatusMsg) {
      tournamentStatusMsg.innerText = message;
    }
}
