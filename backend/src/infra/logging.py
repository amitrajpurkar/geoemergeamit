from __future__ import annotations

import contextvars
import logging


_request_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("request_id", default=None)


def set_request_id(request_id: str | None) -> None:
    _request_id_var.set(request_id)


def get_request_id() -> str | None:
    return _request_id_var.get()


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id() or "-"
        return True


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(level=level)
    root = logging.getLogger()
    for handler in root.handlers:
        handler.addFilter(RequestIdFilter())
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s [req:%(request_id)s] %(message)s")
        )
