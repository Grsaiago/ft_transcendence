const canvas = document.getElementById('pongCanvas');
const context = canvas.getContext('2d');

//draw hello world in the middle of the canvas
context.font = '30px Courier New';
context.fillText('Start', canvas.width / 2 - 100, canvas.height / 2);

//Websocket connection
const socket = new WebSocket('ws://' + window.location.host + '/ws/pong/');

socket.onopen = function (e) {
    console.log('WebSocket connection established');
    socket.send(JSON.stringify({ message: 'pong' }));
}

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log("Message from server: ", data);
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillText(data.message, canvas.width / 2 - 100, canvas.height / 2);
}

socket.onclose = function (e) {
    console.log('WebSocket connection closed');
}
