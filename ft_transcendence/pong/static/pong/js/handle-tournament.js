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
const username = gameData.dataset.username

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
};

function handleCurrentState(data) {
    log.info ("handleCurrentState:", data);
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
    type: "join_tournament",
  });
  joinButton.style.display = "none";
}

function sendMessage(message) {
    const jsonMessage = JSON.stringify(message);
    log.debug("Sending message:", jsonMessage);
    socket.send(jsonMessage);
  }

function updateTournamentUI(state) {
  // Atualizar elementos do DOM conforme o estado
  const participantsList = document.getElementById("participantsList");
  const bracketContainer = document.getElementById("bracket-container");

  // Atualizar a lista de participantes
  if (participantsList) {
    participantsList.innerHTML = ""; // Limpar lista anterior
    state.participants.forEach((participant) => {
      const li = document.createElement("li");
      li.innerText = participant;
      participantsList.appendChild(li);
    });
  }

  // // Atualizar a lista de partidas
  // if (matchesList) {
  //   matchesList.innerHTML = ""; // Limpar lista anterior
  //   state.matches.forEach((match) => {
  //     const li = document.createElement("li");
  //     li.classList.add("match-item");

  //     const matchInfo = `
  //       <strong>Match ID:</strong> ${match.id}<br>
  //       <strong>Player 1:</strong> ${match.player1}<br>
  //       <strong>Player 2:</strong> ${match.player2}<br>
  //       <strong>Status:</strong> ${match.finished ? "Finalizada" : "Em andamento"}<br>
  //       ${match.finished ? `<strong>Winner:</strong> ${match.winner}<br>` : ""}
  //     `;

  //     li.innerHTML = matchInfo;

  //     matchesList.appendChild(li);
  //   });
  // }


  // Atualizar o bracket
  if (bracketContainer) {
    bracketContainer.innerHTML = "";

    const maxPlayers = state.max_players;
    let rounds;

    if (maxPlayers === 8) {
      rounds = {
        "Quarter1": "Quartas de Final",
        "Quarter2": "Quartas de Final",
        "Quarter3": "Quartas de Final",
        "Quarter4": "Quartas de Final",
        "Semi1": "Semifinais",
        "Semi2": "Semifinais",
        "Final": "Final",
      };
    } else {
      rounds = {
        "Semi1": "Semifinais",
        "Semi2": "Semifinais",
        "Final": "Final",
      };
    }
    // Preencher os rounds com as partidas
    const organizedRounds = {};

    state.matches.forEach((match) => {
      const roundName = rounds[match.round];
      if (!organizedRounds[roundName]) {
        organizedRounds[roundName] = [];
      }
      organizedRounds[roundName].push(match);
    });

    // Renderizar os rounds em colunar
    const roundOrder = ["Quartas de Final", "Semifinais", "Final"];

    roundOrder.forEach((roundName) => {
      if (organizedRounds[roundName]) {
        const roundDiv = document.createElement("div");
        roundDiv.classList.add("round");

        const roundTitle = document.createElement("h3");
        roundTitle.innerText = roundName;
        roundDiv.appendChild(roundTitle);

        organizedRounds[roundName].forEach((match) => {
          const matchDiv = document.createElement("div");
          matchDiv.classList.add("match");

          matchDiv.innerHTML = `
            <div class="player">${match.player1 !== "TBD" ? match.player1 : "Aguardando..."}</div>
            <div class="player">${match.player2 !== "TBD" ? match.player2 : "Aguardando..."}</div>
          `;

          // Adicionar botão para redirecionar para a partida apenas se o username for um dos jogadores
          if ((match.player1 === username || match.player2 === username) &&
              !match.finished && match.player1 !== "Aguardando..." &&
              match.player2 !== "Aguardando...") {
            const playButton = document.createElement("button");
            playButton.innerText = "Ir para a Partida";
            playButton.onclick = () => redirectToMatch(match.room_id);
            matchDiv.appendChild(playButton);
        }

          roundDiv.appendChild(matchDiv);
        });

        bracketContainer.appendChild(roundDiv);
      }
    });
  }
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
