import itertools
import logging
from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.session import engine

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: проверка подключения, прогрев пулов и т.п.
    yield
    # shutdown

    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)
logger = logging.getLogger("app.middleware")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
_request_counter = itertools.count(1)


@app.middleware("http")
async def log_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    started_at = perf_counter()
    number = next(_request_counter)
    try:
        response: Response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        client = request.client.host if request.client else "unknown"
        logger.exception(
            "Request #%d from %s failed: %s %s completed_in=%.2fms",
            number,
            client,
            request.method,
            request.url,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started_at) * 1000
    response.headers["X-Request-Number"] = str(number)
    client = request.client.host if request.client else "unknown"
    logger.info(
        "Request #%d from %s: %s %s -> %s (%.2f ms)",
        number,
        client,
        request.method,
        request.url,
        response.status_code,
        duration_ms,
    )
    return response


app.include_router(api_router)
