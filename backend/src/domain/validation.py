from __future__ import annotations

from datetime import date, datetime

from backend.src.domain.errors import InvalidDateRangeError
from backend.src.domain.models import DateRange


def parse_iso_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as e:
        raise InvalidDateRangeError("Invalid date format; expected YYYY-MM-DD") from e


def validate_date_range(date_range: DateRange, *, allow_future: bool = False) -> None:
    if date_range.start_date > date_range.end_date:
        raise InvalidDateRangeError("start_date must be <= end_date")

    if not allow_future and date_range.end_date > date.today():
        raise InvalidDateRangeError("end_date cannot be in the future")
