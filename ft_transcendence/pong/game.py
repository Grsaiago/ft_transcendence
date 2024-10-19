from typing import Any, Dict, Optional

X = "x"
Y = "y"
RIGHT = "right"
LEFT = "left"
UP = "up"
DOWN = "down"
WIDTH = 15
SPEED = 5


class Ball:
    def __init__(self, width: int, height: int) -> None:
        self.size: int = WIDTH
        self.base_speed: int = SPEED
        self.x_start: int = width // 2 - self.size // 2
        self.y_start: int = height // 2 - self.size // 2
        self.x: int = self.x_start
        self.y: int = self.y_start
        self.x_speed: int = self.base_speed
        self.y_speed: int = self.base_speed

    def move(self) -> None:
        self.x += self.x_speed
        self.y += self.y_speed

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
        self.players: Dict[int, str] = {}
        self.score: Dict[int, int] = {}
        self.winner: Optional[int] = None
        self.started: bool = False
        self.finished: bool = False

    def add_player(self, user_id: int, user_name: str) -> None:
        self.players[user_id] = user_name
        self.score[user_id] = 0

    def remove_player(self, user_id: int) -> None:
        if user_id in self.players:
            del self.players[user_id]
            del self.score[user_id]

    def update_score(self, user_id: int) -> None:
        self.score[user_id] += 1
        if self.score[user_id] == 10:
            self.winner = user_id
            self.finished = True

    def start_game(self) -> None:
        self.started = True

    def stop_game(self) -> None:
        self.started = False

    def game_loop(self) -> None:
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
            "players": {
                str(player_id): name for player_id, name in self.players.items()
            },
            "score": {str(player_id): score for player_id, score in self.score.items()},
            "winner": str(self.winner) if self.winner is not None else None,
            "started": self.started,
            "finished": self.finished,
        }
