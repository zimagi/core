"""
Zimagi ASGI config.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django

from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Mount, Route
from systems.api.mcp.auth import TokenAuthBackend
from systems.api.mcp.routes import get_connection_handler, get_connection_lifespan, handle_status
from systems.models.overrides import *  # noqa: F401, F403
from utility.mutex import Mutex


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.full")
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

django.setup()

server = Server("zimagi-mcp")
session_manager = StreamableHTTPSessionManager(
    app=server,
    event_store=None,
    json_response=True,
    stateless=True,
)


def get_asgi_application():
    from django.conf import settings

    return Starlette(
        debug=settings.DEBUG,
        routes=[
            Route("/status", endpoint=handle_status, methods=["GET"]),
            Mount("/", app=get_connection_handler(server, session_manager)),
        ],
        lifespan=get_connection_lifespan(session_manager),
        middleware=[Middleware(AuthenticationMiddleware, backend=TokenAuthBackend())],
    )


#
# Application Initialization
#
application = get_asgi_application()

Mutex.set("startup_{}".format(os.environ["ZIMAGI_SERVICE"]))
