"""Retry mechanism with exponential backoff."""
import functools
import logging
import time
from typing import Callable, Type, Tuple, Union, Any, Optional

from autopaper.utils.logging import get_logger

logger = get_logger(__name__)


def retry(
    max_attempts: int = 3,
    backoff_factor: float = 2.0,
    initial_delay: float = 1.0,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
    on_retry: Optional[Callable] = None,
    logger_instance: Optional[logging.Logger] = None
) -> Callable:
    """Decorator for retrying functions with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        backoff_factor: Multiplier for delay between retries (default: 2.0)
        initial_delay: Initial delay in seconds before first retry (default: 1.0)
        exceptions: Exception(s) to catch and retry on (default: Exception)
        on_retry: Optional callback function called on each retry
        logger_instance: Optional logger instance (uses module logger if not provided)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3, exceptions=(requests.RequestException,))
        >>> def fetch_url(url):
        >>>     return requests.get(url, timeout=30)

        >>> @retry(max_attempts=5, backoff_factor=1.5)
        >>> def call_ai_api(prompt):
        >>>     return anthropic.messages.create(...)
    """
    _logger = logger_instance or logger

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            delay = initial_delay

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e

                    # If this was the last attempt, raise the exception
                    if attempt == max_attempts - 1:
                        _logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts: {e}"
                        )
                        raise

                    # Log the retry
                    _logger.warning(
                        f"{func.__name__} failed (attempt {attempt + 1}/{max_attempts}): {e}. "
                        f"Retrying in {delay:.1f}s..."
                    )

                    # Call on_retry callback if provided
                    if on_retry:
                        try:
                            on_retry(attempt + 1, e)
                        except Exception as callback_error:
                            _logger.error(f"on_retry callback failed: {callback_error}")

                    # Sleep before next attempt
                    time.sleep(delay)

                    # Increase delay for next attempt (exponential backoff)
                    delay *= backoff_factor

            # Should never reach here, but just in case
            if last_exception:
                raise last_exception

        return wrapper
    return decorator


class RetryContext:
    """Context manager for retrying code blocks.

    Examples:
        >>> with RetryContext(max_attempts=3) as retry:
        >>>     while retry.should_retry():
        >>>         try:
        >>>             result = risky_operation()
        >>>             break
        >>>         except Exception as e:
        >>>             retry.record_failure(e)
    """

    def __init__(
        self,
        max_attempts: int = 3,
        backoff_factor: float = 2.0,
        initial_delay: float = 1.0,
        exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception
    ):
        self.max_attempts = max_attempts
        self.backoff_factor = backoff_factor
        self.initial_delay = initial_delay
        self.exceptions = exceptions
        self.attempt = 0
        self.last_exception = None
        self.delay = initial_delay

    def should_retry(self) -> bool:
        """Check if we should retry."""
        return self.attempt < self.max_attempts

    def record_failure(self, exception: Exception) -> None:
        """Record a failed attempt."""
        if not isinstance(exception, self.exceptions):
            raise exception

        self.last_exception = exception
        self.attempt += 1

        if self.attempt < self.max_attempts:
            logger.warning(
                f"Operation failed (attempt {self.attempt}/{self.max_attempts}): {exception}. "
                f"Retrying in {self.delay:.1f}s..."
            )
            time.sleep(self.delay)
            self.delay *= self.backoff_factor
        else:
            logger.error(
                f"Operation failed after {self.max_attempts} attempts: {exception}"
            )

    def __enter__(self) -> 'RetryContext':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and self.attempt >= self.max_attempts:
            # Re-raise the exception if we exhausted all retries
            return False
        return True
