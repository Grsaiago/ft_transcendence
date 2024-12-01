import { PongGame } from "./PongGame.js";

//Get canvas and context
const canvas = document.getElementById("pongCanvas");
const context = canvas.getContext("2d");

//Initialize game
const pongGame = new PongGame(context, canvas.width, canvas.height);

//Get game data
const gameData = document.getElementById("game-data");
const room_id = gameData.dataset.roomId;
const game_mode = gameData.dataset.gameMode;

console.log("room_id:", room_id);
console.log("game_mode:", game_mode);

//Websocket connection
const socketUrl = `ws://${window.location.host}/ws/pong/${game_mode}/`;
const socket = new WebSocket(socketUrl);

socket.onopen = function (e) {
  const message = JSON.stringify({
    type: "join_room",
    room_id: room_id,
    width: canvas.width,
    height: canvas.height,
  });
  //console.log('Sending message:', message);
  socket.send(message);
  console.log("WebSocket connection established");
};

socket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  //console.log("Message from server: ", data);
  //console.log("data type: ", data.type);

  if (data.type ==="not_auth") {
    alert(data.message);
    //redirect to login page
    socket.close();
  }

  if (data.type === "game_init") {
    pongGame.drawGameState(data.game_state);
  }

  if (data.type === "update_game_state") {
    pongGame.drawGameState(data.game_state);
  }

  if (data.type === "start_game") {
    const startButton = document.getElementById("startGame");
    startButton.style.display = "none";
    const messageContainer = document.getElementById("messageContainer");
    messageContainer.textContent = "Game started";
    console.log("Game started");
  }

  if (data.type ==="winner") {
    const messageContainer = document.getElementById("messageContainer");
    messageContainer.textContent = data.winner + " wins!";
    const startButton = document.getElementById("startGame");
    startButton.style.display = "block";
  }

};

socket.onclose = function (e) {
  console.log("WebSocket connection closed", e.code);
};

// button start game event listener
const startButton = document.getElementById("startGame");
startButton.addEventListener("click", function () {
  const message = JSON.stringify({
    type: "start_game",
  });
  console.log("Sending message:", message);
  socket.send(message);
});

// keydown event listener
document.addEventListener("keydown", function (event) {
  if (
    event.key === "ArrowUp" ||
    event.key === "ArrowDown" ||
    event.key === "w" ||
    event.key === "s" ||
    event.key === "W" ||
    event.key === "S"
  ) {
    event.preventDefault();
    const message = JSON.stringify({
      type: "keydown",
      key: event.key.toLocaleLowerCase(),
    });
    //console.log('Sending message:', message);
    socket.send(message);
  }
});

// keyup event listener
document.addEventListener("keyup", function (event) {
  if (
    event.key === "ArrowUp" ||
    event.key === "ArrowDown" ||
    event.key === "w" ||
    event.key === "s" ||
    event.key === "W" ||
    event.key === "S"
  ) {
    event.preventDefault();
    const message = JSON.stringify({
      type: "keyup",
      key: event.key.toLocaleLowerCase(),
    });
    //console.log('Sending message:', message);
    socket.send(message);
  }
});
