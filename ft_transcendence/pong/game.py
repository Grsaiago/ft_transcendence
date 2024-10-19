X = "x"
Y = "y"
RIGHT = "right"
LEFT = "left"
UP = "up"
DOWN = "down"


class Ball:
    def __init__(self, width, height) -> None:
        self.size = 15
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


class PongGame:
    def __init__(self, width, height) -> None:
        self.players = {}
        self.score = {}
        self.ball = Ball(width, height)
        self.width = width
        self.height = height
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
            "players": self.players,
            "score": self.score,
            "ball": {
                "x": self.ball.x,
                "y": self.ball.y,
                "size": self.ball.size,
            },
            "width": self.width,
            "height": self.height,
            "winner": self.winner,
            "started": self.started,
            "finished": self.finished,
        }
