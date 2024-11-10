from .base_consumer import BasePongConsumer


class LocalPongConsumer(BasePongConsumer):
    async def handle_key_paddle_event(self, key, state):
        # mapeia as para os paddle no modo local
        # w e s para o paddle esquerdo
        # arrowup e arrowdown para o paddle direito
        if key in ["w", "s"]:
            paddle = "left"
            direction = "up" if key == "w" else "down"
        elif key in ["arrowup", "arrowdown"]:
            paddle = "right"
            direction = "up" if key == "arrowup" else "down"

        await self.worker_update_paddles_position(paddle, direction, state)
