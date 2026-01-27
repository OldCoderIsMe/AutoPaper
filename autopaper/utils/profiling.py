"""Performance profiling utilities."""
import functools
import time
import logging
from typing import Callable, Any

from autopaper.utils.logging import get_logger

logger = get_logger(__name__)


class ProfilerStats:
    """Statistics collector for profiling."""

    def __init__(self):
        self.calls = {}
        self.total_times = {}

    def record(self, func_name: str, elapsed: float):
        """Record a function call."""
        if func_name not in self.calls:
            self.calls[func_name] = 0
            self.total_times[func_name] = 0.0

        self.calls[func_name] += 1
        self.total_times[func_name] += elapsed

    def get_stats(self, func_name: str) -> dict:
        """Get statistics for a function."""
        if func_name not in self.calls:
            return {}

        return {
            "calls": self.calls[func_name],
            "total_time": self.total_times[func_name],
            "avg_time": self.total_times[func_name] / self.calls[func_name],
        }

    def get_all_stats(self) -> dict:
        """Get statistics for all functions."""
        return {
            func_name: self.get_stats(func_name)
            for func_name in self.calls
        }

    def print_summary(self):
        """Print a summary of all profiling data."""
        if not self.calls:
            logger.info("No profiling data available")
            return

        logger.info("=" * 60)
        logger.info("Performance Summary")
        logger.info("=" * 60)

        # Sort by total time
        sorted_funcs = sorted(
            self.total_times.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for func_name, total_time in sorted_funcs:
            stats = self.get_stats(func_name)
            logger.info(
                f"{func_name}: {stats['calls']} calls, "
                f"{total_time:.2f}s total, "
                f"{stats['avg_time']:.3f}s avg"
            )

        logger.info("=" * 60)


# Global profiler instance
_profiler = ProfilerStats()


def profile(
    log_slow_calls: float = 5.0,
    log_all_calls: bool = False,
    enabled: bool = True
) -> Callable:
    """Decorator for profiling function execution time.

    Args:
        log_slow_calls: Log warning if function takes longer than this (seconds)
        log_all_calls: Log info for every call
        enabled: Enable profiling (can be disabled for production)

    Returns:
        Decorated function with profiling

    Examples:
        >>> @profile(log_slow_calls=2.0)
        >>> def expensive_function():
        >>>     # Do something expensive
        >>>     pass

        >>> @profile(log_all_calls=True)
        >>> def debug_function():
        >>>     # Log every call
        >>>     pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not enabled:
                return func(*args, **kwargs)

            start = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed = time.time() - start
                _profiler.record(func.__name__, elapsed)

                # Log slow calls
                if elapsed > log_slow_calls:
                    logger.warning(
                        f"{func.__name__} is slow (> {log_slow_calls}s): "
                        f"took {elapsed:.2f}s"
                    )
                elif log_all_calls:
                    logger.debug(f"{func.__name__} took {elapsed:.3f}s")

        return wrapper
    return decorator


def get_profiler_stats() -> dict:
    """Get all profiling statistics.

    Returns:
        Dictionary of profiling data
    """
    return _profiler.get_all_stats()


def print_profiler_summary():
    """Print a summary of profiling data."""
    _profiler.print_summary()


def clear_profiler_stats():
    """Clear all profiling data."""
    _profiler.calls.clear()
    _profiler.total_times.clear()
    logger.info("Profiler statistics cleared")


class TimeContext:
    """Context manager for timing code blocks.

    Examples:
        >>> with TimeContext("database query"):
        >>>     # Execute query
        >>>     results = db.execute("SELECT * FROM articles")
    """

    def __init__(self, name: str, log_threshold: float = 1.0):
        """Initialize timing context.

        Args:
            name: Name of the operation being timed
            log_threshold: Log warning if operation takes longer than this
        """
        self.name = name
        self.log_threshold = log_threshold
        self.start_time = None

    def __enter__(self) -> 'TimeContext':
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time

        if elapsed > self.log_threshold:
            logger.warning(
                f"[SLOW] {self.name} took {elapsed:.2f}s "
                f"(threshold: {self.log_threshold}s)"
            )
        else:
            logger.debug(f"{self.name} took {elapsed:.3f}s")
