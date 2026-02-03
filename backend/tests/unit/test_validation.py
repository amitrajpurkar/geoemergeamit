from __future__ import annotations

from datetime import date, timedelta

import pytest

from backend.src.domain.errors import InvalidDateRangeError
from backend.src.domain.models import DateRange
from backend.src.domain.validation import validate_date_range


def test_validate_date_range_rejects_reversed() -> None:
    dr = DateRange(start_date=date(2020, 1, 2), end_date=date(2020, 1, 1))
    with pytest.raises(InvalidDateRangeError):
        validate_date_range(dr)


def test_validate_date_range_rejects_future_end_date() -> None:
    dr = DateRange(start_date=date.today(), end_date=date.today() + timedelta(days=1))
    with pytest.raises(InvalidDateRangeError):
        validate_date_range(dr)


def test_validate_date_range_accepts_valid() -> None:
    dr = DateRange(start_date=date(2020, 1, 1), end_date=date(2020, 1, 2))
    validate_date_range(dr)
