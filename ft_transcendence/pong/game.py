X = "x"
Y = "y"
RIGHT = "right"
LEFT = "left"
UP = "up"
DOWN = "down"
WIDTH = 15


class Ball:
    def __init__(self, width, height) -> None:
        self.size = WIDTH
        self.base_speed = 1
        self.x_start = width // 2 - self.size // 2
        self.y_start = height // 2 - self.size // 2
        self.x = self.x_start
        self.y = self.y_start
        self.x_speed = self.base_speed
        self.y_speed = self.base_speed

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def reset(self):
        self.x = self.x_start
        self.y = self.y_start
        self.vx = self.base_speed
        self.vy = self.base_speed


class Paddle:
    def __init__(self, width, height, side) -> None:
        self.width = WIDTH
        self.height = WIDTH * 8
        self.y = height // 2 - self.height // 2
        if side == LEFT:
            self.x = WIDTH * 2
        else:
            self.x = width - self.width - (WIDTH * 2)
        self.speed = 1

    def move(self, direction):
        if direction == UP:
            self.y -= self.speed
        elif direction == DOWN:
            self.y += self.speed


class PongGame:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.ball = Ball(width, height)
        self.paddle_left = Paddle(width, height, LEFT)
        self.paddle_right = Paddle(width, height, RIGHT)
        self.players = {}
        self.score = {}
        self.winner = None
        self.started = False
        self.finished = False

    def add_player(self, user_id, user_name):
        self.players[user_id] = user_name
        self.score[user_id] = 0

    def remove_player(self, user_id):
        if user_id in self.players:
            del self.players[user_id]
            del self.score[user_id]

    def update_score(self, user_id):
        self.score[user_id] += 1
        if self.score[user_id] == 10:
            self.winner = user_id
            self.finished = True

    def get_game_state(self):
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
            "players": self.players,
            "score": self.score,
            "winner": self.winner,
            "started": self.started,
            "finished": self.finished,
        }
