import time
from backend.logger import logger

class CycleGuard:

    def __init__(self):
        self.last_valid_cycle_time = 0
        self.consecutive_empty_cycles = 0
        self.max_empty_cycles = 3
        self.cooldown_seconds = 60

    def should_skip_cycle(self, data):
        """
        TRUE → cycle SKIP
        FALSE → cycle OK
        """

        if data:
            self.consecutive_empty_cycles = 0
            self.last_valid_cycle_time = time.time()
            return False

        self.consecutive_empty_cycles += 1

        logger.warning(
            f"[CYCLE GUARD] empty cycle #{self.consecutive_empty_cycles}"
        )

        # too many empty cycles → cooldown mode
        if self.consecutive_empty_cycles >= self.max_empty_cycles:
            if time.time() - self.last_valid_cycle_time < self.cooldown_seconds:
                logger.warning("[CYCLE GUARD] cooldown active → skipping cycle")
                return True

        return False
