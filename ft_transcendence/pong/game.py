import random
from typing import Any, Dict, Optional

THICKNESS = 15
BALL_SPEED = 1
PADDLE_SPEED = BALL_SPEED * 2
X = "x"
Y = "y"
RIGHT = "right"
LEFT = "left"
UP = "up"
DOWN = "down"
STOP = "stop"


class Ball:
    def __init__(self, width: int, height: int) -> None:
        """
        Ball class constructor.
        x and y coordinates are defined relative to the top-left corner.
        """
        self.size: int = THICKNESS
        self.center: float = float(self.size / 2)
        self.base_speed: int = BALL_SPEED
        self.x_start: float = float(width / 2) - self.center
        self.y_start: float = float(height / 2) - self.center
        self.y_min_start: int = 6 * THICKNESS
        self.y_max_start: int = height - (6 * THICKNESS)
        self.x: float = self.x_start
        self.y: float = self.y_start
        self.x_speed: float = float(self.base_speed)
        self.y_speed: float = float(self.base_speed)

    def move(self) -> None:
        self.x += self.x_speed
        self.y += self.y_speed

    def bounce(self, direction: str) -> None:
        if direction == X:
            self.x_speed *= -1
        elif direction == Y:
            self.y_speed *= -1

    def check_boundaries(self, width: int, height: int) -> None:
        if self.y <= (0 + THICKNESS) or self.y + self.size >= (height - THICKNESS):
            self.bounce(Y)
        if self.x <= 0 or self.x + self.size >= width:
            self.reset()
            if random.randint(0, 1) == 0:
                self.bounce(X)

    def check_paddles_collisions(
        self, paddle_left: "Paddle", paddle_right: "Paddle"
    ) -> None:
        if (
            self.x <= paddle_left.x + paddle_left.width
            and paddle_left.y <= self.y <= paddle_left.y + paddle_left.height
        ) or (
            self.x + self.size >= paddle_right.x
            and paddle_right.y <= self.y <= paddle_right.y + paddle_right.height
        ):
            self.bounce(X)

    def reset(self):
        self.x = self.x_start
        self.y = float(random.randint(self.y_min_start, self.y_max_start))
        self.x_speed = self.base_speed
        self.y_speed = self.base_speed


class Paddle:
    def __init__(self, width: int, height: int, side: str) -> None:
        self.width: int = THICKNESS
        self.height: int = 120
        self.top_limit: int = THICKNESS
        self.bottom_limit: int = height - self.height - THICKNESS
        self.y: float = float(height / 2) - (self.height / 2)
        if side == LEFT:
            self.x: float = float(THICKNESS * 2)
        else:
            self.x: float = float(width - self.width - (THICKNESS * 2))
        self.speed: int = 0

    def move(self, direction: str) -> None:
        if direction == UP:
            self.speed = -PADDLE_SPEED
        elif direction == DOWN:
            self.speed = PADDLE_SPEED
        elif direction == STOP:
            self.speed = 0

    def limit(self) -> None:
        if self.y <= self.top_limit:
            self.y = self.top_limit

        if self.y >= self.bottom_limit:
            self.y = self.bottom_limit

    def movement(self) -> None:
        self.y += self.speed
        self.limit()


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

    def paddle_on(self, key: str) -> None:
        if key == "arrowup":
            self.paddle_right.move(UP)
        elif key == "arrowdown":
            self.paddle_right.move(DOWN)
        elif key == "w":
            self.paddle_left.move(UP)
        elif key == "s":
            self.paddle_left.move(DOWN)

    def paddle_off(self, key: str) -> None:
        if key == "arrowup" or key == "arrowdown":
            self.paddle_right.move(STOP)
        if key == "w" or "s":
            self.paddle_left.move(STOP)

    def game_loop(self) -> None:
        self.ball.check_boundaries(self.width, self.height)
        self.paddle_left.movement()
        self.paddle_right.movement()
        self.ball.check_paddles_collisions(self.paddle_left, self.paddle_right)
        self.ball.move()

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
