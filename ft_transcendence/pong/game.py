import random
from typing import Dict, Optional, TypedDict

THICKNESS = 15
BALL_SPEED = 5
PADDLE_SPEED = BALL_SPEED * 2
X = "x"
Y = "y"
RIGHT = "right"
LEFT = "left"
UP = "up"
DOWN = "down"
STOP = "stop"


class BallPosition(TypedDict):
    x: float
    y: float
    size: int
    center: float
    x_speed: float
    y_speed: float


class PaddlePosition(TypedDict):
    x: float
    y: float
    width: int
    height: int


class GameState(TypedDict):
    width: int
    height: int
    ball: BallPosition
    paddle_left: PaddlePosition
    paddle_right: PaddlePosition
    players: Dict[str, str]
    score: Dict[str, int]
    winner: Optional[int]
    started: bool
    finished: bool


class Ball:
    def __init__(self, width: int, height: int) -> None:
        """
        Ball class constructor. Initializes the ball's size, position, and speed.
        Self x and y coordinates are defined relative to the top-left corner.

        Args:
            width (int): The width of game are from canvas.
            height (int): The height of the game area from canvas.
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

    async def move(self) -> None:
        """
        Updates the ball's position based on its current speed.
        """
        self.x += self.x_speed
        self.y += self.y_speed

    async def bounce(self, direction: str) -> None:
        """
        Reverses the ball's speed in the given direction.

        Args:
            direction (str): The direction in which to reverse the ball's speed ('x' or 'y').
        """
        if direction == X:
            self.x_speed *= -1
        elif direction == Y:
            self.y_speed *= -1

    async def reset(self):
        """
        Reset the ball to the center of the game area with a random y position and speed.
        """
        print("enter in reset ball")
        self.x = self.x_start
        self.y = float(random.randint(self.y_min_start, self.y_max_start))
        self.x_speed = self.base_speed
        self.y_speed = self.base_speed
        if random.randint(0, 1) == 0:
            await self.bounce(X)


class Paddle:
    def __init__(self, width: int, height: int, side: str) -> None:
        """
        Paddle class constructor. Initializes the paddle's position, size, and movement speed.

        Args:
            width (int): The width of the game area.
            height (int): The height of the game area.
            side (str): The side the paddle is on ('left' or 'right').
        """
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

    async def set_speed(self, direction: str) -> None:
        """
        Sets the paddle's speed based on the direction of movement.

        Args:
            direction (str): The direction to move the paddle ('up', 'down', or 'stop').
        """
        if direction == UP:
            self.speed = -PADDLE_SPEED
        elif direction == DOWN:
            self.speed = PADDLE_SPEED
        elif direction == STOP:
            self.speed = 0

    async def limit(self) -> None:
        """
        Limits the paddle's movement to prevent it from moving outside the game area.
        """
        if self.y <= self.top_limit:
            self.y = self.top_limit

        if self.y >= self.bottom_limit:
            self.y = self.bottom_limit

    async def move(self) -> None:
        """
        Updates the paddle's position based on its speed and applies movement limits.
        """
        self.y += self.speed
        await self.limit()


class PongGame:
    def __init__(self, width: int, height: int) -> None:
        """
        PongGame class constructor. Initializes the game area, ball, and paddles.

        Args:
            width (int): The width of the game area.
            height (int): The height of the game area.
        """
        self.width: int = width
        self.height: int = height
        self.ball: Ball = Ball(width, height)
        self.paddle_left: Paddle = Paddle(width, height, LEFT)
        self.paddle_right: Paddle = Paddle(width, height, RIGHT)
        self.score: Dict[str, int] = {"left": 0, "right": 0}
        self.winner: Optional[str] = None

    async def update_score(self, side: str) -> None:
        """
        Updates the score for the given side and checks if a player has won.
        """
        self.score[side] += 1
        if self.score[side] == 3:
            self.winner = side

    async def paddle_on(self, key: str) -> None:
        """
        Activates the paddle's movement based on the key pressed.

        Args:
            key (str): The key pressed by the player ('arrowup', 'arrowdown', 'w', 's').
        """
        if key == "arrowup":
            await self.paddle_right.set_speed(UP)
        elif key == "arrowdown":
            await self.paddle_right.set_speed(DOWN)
        elif key == "w":
            await self.paddle_left.set_speed(UP)
        elif key == "s":
            await self.paddle_left.set_speed(DOWN)

    async def paddle_off(self, key: str) -> None:
        """
        Stops the paddle's movement when the key is released.

        Args:
            key (str): The key released by the player ('arrowup', 'arrowdown', 'w', 's').
        """
        if key in ["arrowup", "arrowdown"]:
            await self.paddle_right.set_speed(STOP)
        if key in ["w", "s"]:
            await self.paddle_left.set_speed(STOP)

    async def calculate_ball_colision(self) -> None:
        """
        Checks if the ball hits the top or bottom boundaries and bounces it.
        Resets the ball if it hits the left or right boundaries.
        """
        if self.ball.y <= THICKNESS or self.ball.y + self.ball.size >= (
            self.height - THICKNESS
        ):
            await self.ball.bounce(Y)
        if self.ball.x <= 0:
            await self.update_score(RIGHT)
            await self.ball.reset()
        if self.ball.x + self.ball.size >= self.width:
            await self.update_score(LEFT)
            await self.ball.reset()

    async def calculate_paddle_colision(self) -> None:
        """
        Checks if the ball hits the paddles and bounces it.
        """
        if (
            self.paddle_left.x
            <= self.ball.x
            <= self.paddle_left.x + self.paddle_left.width
            and self.paddle_left.y
            <= self.ball.y
            <= self.paddle_left.y + self.paddle_left.height
        ):
            await self.ball.bounce(X)
        if (
            self.paddle_right.x
            <= self.ball.x + self.ball.size
            <= self.paddle_right.x + self.paddle_right.width
            and self.paddle_right.y
            <= self.ball.y
            <= self.paddle_right.y + self.paddle_right.height
        ):
            await self.ball.bounce(X)

    async def check_colisions(self) -> None:
        """
        Checks for collisions between the ball and the paddles.
        """
        await self.calculate_ball_colision()
        await self.calculate_paddle_colision()

    async def move_objects(self) -> None:
        """
        Moves the ball and paddles based on their current speeds.
        """
        await self.ball.move()
        await self.paddle_left.move()
        await self.paddle_right.move()

    async def calculate_game_tick(self) -> GameState:
        """
        Checks for collisions and moves the objects in the game if the game has no winner.
        Returns the current state of the game.
        """
        await self.check_colisions()
        # just do next move if the game is not finished, so don't have a winner
        if not self.has_winner():
            await self.move_objects()
        return await self.get_game_state()

    def has_winner(self) -> bool:
        """
        Checks if a player has reached the winning score.
        """
        return bool(self.winner)

    async def get_game_state(self) -> GameState:
        """
        Returns the current state of the game.
        """
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
            "score": self.score,
            "winner": self.winner,
        }
