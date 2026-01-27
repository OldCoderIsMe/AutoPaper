"""Date utility functions for AutoPaper."""
from datetime import datetime, timedelta
from typing import Tuple


def get_week_range(date: datetime = None) -> Tuple[str, str]:
    """Get the start and end dates of the week for a given date.

    Args:
        date: Date to get week range for (defaults to today)

    Returns:
        Tuple of (start_date, end_date) in ISO format (YYYY-MM-DD)
    """
    if date is None:
        date = datetime.now()

    # Monday is day 0, Sunday is day 6
    # We want Monday as start, Sunday as end
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)

    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


def get_week_id(date: datetime = None) -> str:
    """Get week ID in format YYYY-Www.

    Args:
        date: Date to get week ID for (defaults to today)

    Returns:
        Week ID string (e.g., "2026-W04")
    """
    if date is None:
        date = datetime.now()

    # ISO week number
    week_number = date.isocalendar()[1]
    year = date.year

    return f"{year}-W{week_number:02d}"


def parse_week_id(week_id: str) -> Tuple[str, str]:
    """Parse week ID and return start and end dates.

    Args:
        week_id: Week ID in format YYYY-Www (e.g., "2026-W04")

    Returns:
        Tuple of (start_date, end_date) in ISO format
    """
    try:
        year, week = week_id.split("-W")
        year = int(year)
        week = int(week)

        # Get first day of the year
        jan_1 = datetime(year, 1, 1)

        # Get first Monday of the year
        first_monday = jan_1
        if jan_1.weekday() != 0:
            # If Jan 1 is not Monday, go to next Monday
            days_until_monday = (7 - jan_1.weekday()) % 7
            first_monday = jan_1 + timedelta(days=days_until_monday)

        # Calculate start of the requested week
        start = first_monday + timedelta(weeks=week - 1)
        end = start + timedelta(days=6)

        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid week ID format: {week_id}. Expected format: YYYY-Www (e.g., 2026-W04)") from e


def get_current_week_id() -> str:
    """Get current week ID.

    Returns:
        Current week ID string
    """
    return get_week_id()


def get_last_week_id() -> str:
    """Get last week's ID.

    Returns:
        Last week's ID string
    """
    last_week = datetime.now() - timedelta(weeks=1)
    return get_week_id(last_week)
