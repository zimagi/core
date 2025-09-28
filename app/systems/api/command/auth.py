import logging

from rest_framework import permissions
from systems.api.auth import APITokenAuthentication

logger = logging.getLogger(__name__)


class CommandAPITokenAuthentication(APITokenAuthentication):
    api_type = "command_api"


class CommandPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        from systems.commands.webhook import WebhookCommand

        if isinstance(view.command, WebhookCommand):
            return True
        return view.check_execute(request.user)
