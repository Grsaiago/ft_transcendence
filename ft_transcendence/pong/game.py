from typing import Any, Dict, Optional

WIDTH = 15
SPEED = 1
X = "x"
Y = "y"
RIGHT = "right"
LEFT = "left"
UP = "up"
DOWN = "down"


class Ball:
    def __init__(self, width: int, height: int) -> None:
        self.size: int = WIDTH
        self.center: float = float(self.size // 2)
        self.base_speed: int = SPEED
        self.x_start: float = float(width // 2 - self.center)
        self.y_start: float = float(height // 2 - self.center)
        self.x: float = self.x_start
        self.y: float = self.y_start
        self.x_speed: float = float(self.base_speed)
        self.y_speed: float = float(self.base_speed)

    def move(self) -> None:
        print(f"Ball position move: {self.x}, {self.y}")
        self.x += self.x_speed
        self.y += self.y_speed

    def bounce(self, direction: str) -> None:
        if direction == X:
            self.x_speed *= -1
        elif direction == Y:
            self.y_speed *= -1

    def check_collisions(self, width: int, height: int) -> None:
        print(f"Ball position collisions: {self.x}, {self.y}")
        if self.y <= (0 + WIDTH) or self.y + self.size >= (height - WIDTH):
            self.bounce(Y)
        if self.x <= 0 or self.x + self.size >= width:
            self.bounce(X)

    def reset(self):
        self.x = self.x_start
        self.y = self.y_start
        self.x_speed = self.base_speed
        self.y_speed = self.base_speed


class Paddle:
    def __init__(self, width: int, height: int, side: str) -> None:
        self.width: int = WIDTH
        self.height: int = WIDTH * 8
        self.y: int = height // 2 - self.height // 2
        if side == LEFT:
            self.x: int = WIDTH * 2
        else:
            self.x: int = width - self.width - (WIDTH * 2)
        self.speed: int = 1

    def move(self, direction: str) -> None:
        if direction == UP:
            self.y -= self.speed
        elif direction == DOWN:
            self.y += self.speed


class PongGame:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.ball: Ball = Ball(width, height)
        self.paddle_left: Paddle = Paddle(width, height, LEFT)
        self.paddle_right: Paddle = Paddle(width, height, RIGHT)
        self.players: Dict[str, str] = {}
        self.score: Dict[str, int] = {}
        self.winner: Optional[int] = None
        self.started: bool = False
        self.finished: bool = False

    def add_player(self, user_id: int, user_name: str) -> None:
        self.players[str(user_id)] = user_name
        self.score[str(user_id)] = 0

    def remove_player(self, user_id: int) -> None:
        user_id_str = str(user_id)
        if user_id_str in self.players:
            del self.players[user_id_str]
            del self.score[user_id_str]

    def update_score(self, user_id: int) -> None:
        user_id_str = str(user_id)
        self.score[user_id_str] += 1
        if self.score[user_id_str] == 10:
            self.winner = user_id
            self.finished = True

    def start_game(self) -> None:
        self.started = True

    def stop_game(self) -> None:
        self.started = False

    def game_loop(self) -> None:
        print("Game loop")
        self.ball.check_collisions(self.width, self.height)
        self.ball.move()
        # self.paddle_left.move()
        # self.paddle_right.move()

    def reset_game(self) -> None:
        self.ball.reset()
        self.started = False

    def get_game_state(self) -> Dict[str, Any]:
        return {
            "width": self.width,
            "height": self.height,
            "ball": {
                "x": self.ball.x,
                "y": self.ball.y,
                "size": self.ball.size,
                "center": self.ball.center,
                "x_speed": self.ball.x_speed,
                "y_speed": self.ball.y_speed,
            },
            "paddle_left": {
                "x": self.paddle_left.x,
                "y": self.paddle_left.y,
                "width": self.paddle_left.width,
                "height": self.paddle_left.height,
            },
            "paddle_right": {
                "x": self.paddle_right.x,
                "y": self.paddle_right.y,
                "width": self.paddle_right.width,
                "height": self.paddle_right.height,
            },
            "players": self.players,
            "score": self.score,
            "winner": self.winner,
            "started": self.started,
            "finished": self.finished,
        }
