import contextlib
import logging

from starlette.requests import Request
from starlette.responses import JSONResponse

from .tools import index_tools
from .errors import ServerError


logger = logging.getLogger(__name__)


async def handle_status(request):
    return JSONResponse({"status": "OK"}, status_code=200)


def _initialize_connection(server, request):
    if not request.user.is_authenticated:
        raise ServerError("Access Denied", 401)

    try:
        index_tools(request.user.zimagi, server)

    except Exception as error:
        logger.error(error)
        raise ServerError(f"Initialization failure: {error}")


def get_connection_handler(server, session_manager):
    async def handle_connection(scope, receive, send):
        request = Request(scope, receive=receive)
        try:
            _initialize_connection(server, request)
        except ServerError as error:
            return JSONResponse({"error": str(error)}, status_code=error.code)

        await session_manager.handle_request(scope, receive, send)

    return handle_connection


def get_connection_lifespan(session_manager):

    @contextlib.asynccontextmanager
    async def lifespan(app):
        async with session_manager.run():
            logger.info("Application started with StreamableHTTP session manager!")
            try:
                yield
            finally:
                logger.info("Application shutting down...")

    return lifespan
