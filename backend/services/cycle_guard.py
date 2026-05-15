import time
from backend.logger import logger


class CycleGuard:

    def __init__(self):
        self.empty_cycles = 0
        self.max_empty_cycles = 3
        self.cooldown_seconds = 60
        self.last_valid_cycle = time.time()

    def should_block(self, data):
        """
        True  → cycle BLOCKED
        False → cycle ALLOWED
        """

        if data:
            self.empty_cycles = 0
            self.last_valid_cycle = time.time()
            return False

        self.empty_cycles += 1

        logger.warning(
            f"[CYCLE GUARD] empty cycle {self.empty_cycles}"
        )

        if self.empty_cycles >= self.max_empty_cycles:
            if time.time() - self.last_valid_cycle < self.cooldown_seconds:
                logger.warning("[CYCLE GUARD] cooldown active → blocking cycle")
                return True

        return False
