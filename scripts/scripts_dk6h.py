import logging

logger = logging.getLogger(__name__)


def retry(func, max_attempts: int = 3, delay: float = 1.0):
    import time
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except Exception as exc:
            logger.warning("Attempt %d/%d failed: %s", attempt, max_attempts, exc)
            if attempt == max_attempts:
                raise
            time.sleep(delay)

# 2026-04-24 13:53:08
