from __future__ import annotations

import time
from collections import defaultdict, deque
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from backend.src.infra.logging import set_request_id


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("x-request-id") or str(uuid4())
        set_request_id(rid)
        start = time.time()
        try:
            resp: Response = await call_next(request)
        finally:
            set_request_id(None)
        resp.headers["x-request-id"] = rid
        resp.headers["x-response-time-ms"] = f"{(time.time() - start) * 1000.0:.1f}"
        return resp


class BasicRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, requests_per_minute: int = 120):
        super().__init__(app)
        self._rpm = requests_per_minute
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        client = request.client.host if request.client else "unknown"
        now = time.time()
        q = self._hits[client]
        cutoff = now - 60.0
        while q and q[0] < cutoff:
            q.popleft()
        if len(q) >= self._rpm:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
        q.append(now)
        return await call_next(request)
