from __future__ import annotations


class DomainError(Exception):
    pass


class InvalidLocationError(DomainError):
    pass


class InvalidDateRangeError(DomainError):
    pass


class DataUnavailableError(DomainError):
    pass
