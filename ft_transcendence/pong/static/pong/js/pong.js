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

        context.fillStyle = 'gray';


        const ball = data.game_state.ball;
        context.fillRect(0, 0, canvas.width, ball.size);
        context.fillRect(0, canvasHeight-ball.size, canvas.width, ball.size);

        context.beginPath();
        context.setLineDash([ball.size, ball.size]);
        context.moveTo(canvasWidth/2, 0);
        context.lineTo(canvasWidth/2, canvasHeight);
        context.lineWidth = ball.size;
        context.strokeStyle = context.fillStyle;
        context.stroke();
        context.setLineDash([]);

        context.fillRect(ball.x, ball.y, ball.size, ball.size);

        const paddle_left = data.game_state.paddle_left;
        context.fillRect(paddle_left.x, paddle_left.y, paddle_left.width, paddle_left.height);

        const paddle_right = data.game_state.paddle_right;
        context.fillRect(paddle_right.x, paddle_right.y, paddle_right.width, paddle_right.height);

    }


}

socket.onclose = function (e) {
    console.log('WebSocket connection closed');
}
