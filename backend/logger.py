import logging
import sys

# =====================================================
# LOGGER NAME
# =====================================================
LOGGER_NAME = "dynamohive"


# =====================================================
# FORMATTER
# =====================================================
formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


# =====================================================
# LOGGER INSTANCE
# =====================================================
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)
logger.propagate = False


# =====================================================
# SAFETY: REMOVE OLD HANDLERS (IMPORTANT UPGRADE)
# =====================================================
if logger.hasHandlers():
    logger.handlers.clear()


# =====================================================
# CONSOLE HANDLER
# =====================================================
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


# =====================================================
# OPTIONAL HELPERS
# =====================================================
def info(msg: str):
    logger.info(msg)

def error(msg: str):
    logger.error(msg)

def warning(msg: str):
    logger.warning(msg)

def debug(msg: str):
    logger.debug(msg)
