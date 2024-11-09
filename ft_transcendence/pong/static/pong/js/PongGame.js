const TABLE_COLOR = 'black';
const LINE_COLOR = 'gray';
const BALL_COLOR = LINE_COLOR;
const PADDLE_COLOR = LINE_COLOR;

export class PongGame {
    constructor(context, canvasWidth, canvasHeight) {
        this.context = context;
        this.canvasWidth = canvasWidth;
        this.canvasHeight = canvasHeight;
    }

    clearCanvas() {
        this.context.clearRect(0, 0, this.canvasWidth, this.canvasHeight);
        this.context.fillStyle = TABLE_COLOR
        this.context.fillRect(0, 0, this.canvasWidth, this.canvasHeight);
    }

    drawHorizontalLine(y, thickness) {
        this.context.fillRect(0, y, this.canvasWidth, thickness);
    }

    drawVerticalDashLine(x, thickness) {
        this.context.beginPath();
        this.context.setLineDash([thickness, thickness]);
        this.context.moveTo(x, 0);
        this.context.lineTo(x, this.canvasHeight);
        this.context.lineWidth = thickness;
        this.context.strokeStyle = LINE_COLOR;
        this.context.stroke();
        this.context.setLineDash([]);
    }

    drawTable(thickness) {
        this.context.fillStyle = LINE_COLOR;
        this.drawHorizontalLine(0, thickness);
        this.drawHorizontalLine(this.canvasHeight - thickness, thickness);
        this.drawVerticalDashLine(this.canvasWidth / 2, thickness);
    }

    drawBall(ball) {
        this.context.fillStyle = BALL_COLOR;
        this.context.fillRect(ball.x, ball.y, ball.size, ball.size);
    }

    drawPaddle(paddle) {
        this.context.fillStyle = PADDLE_COLOR;
        this.context.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
    }


    drawGameState(gameState) {
        this.clearCanvas();
        this.drawTable(gameState.ball.size);
        this.drawBall(gameState.ball);
        this.drawPaddle(gameState.paddle_left);
        this.drawPaddle(gameState.paddle_right);
    }
}
