const canvas = document.getElementById('pongCanvas');
const context = canvas.getContext('2d');
const canvasWidth = canvas.width;
const canvasHeight = canvas.height;
const gameData = document.getElementById('game-data');
const room_id = gameData.dataset.roomId

console.log('room_id:', room_id);

//Websocket connection
const socket = new WebSocket('ws://' + window.location.host + '/ws/pong/');

socket.onopen = function (e) {
    const message = JSON.stringify({
        type: "join_room",
        room_id: room_id,
        width: canvasWidth,
        height: canvasHeight
    });
    console.log('Sending message:', message);  // Adicione esta linha
    socket.send(message);
    console.log('WebSocket connection established');
}

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log("Message from server: ", data);
    console.log("data type: ", data.type);

    if (data.type === "game_init") {
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.fillStyle = 'black';
        context.fillRect(0, 0, canvas.width, canvas.height);

        context.fillStyle = 'white';

        const ball = data.game_state.ball;
        context.fillRect(ball.x, ball.y, ball.size, ball.size);

    }


}

socket.onclose = function (e) {
    console.log('WebSocket connection closed');
}
