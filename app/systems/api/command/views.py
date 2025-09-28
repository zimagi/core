import logging

from django.http import StreamingHttpResponse, HttpResponse
from rest_framework.views import APIView
from systems.api.views import wrap_api_call
from systems.encryption.cipher import Cipher
from utility.data import normalize_value

logger = logging.getLogger(__name__)


class Command(APIView):
    name = None
    command = None

    @property
    def schema(self):
        return self.command.get_schema()

    def get_host(self):
        return self.command.get_host()

    def get_resource(self):
        return getattr(self.command, "_resource", None)

    def check_execute(self, user):
        return self.command.check_execute(user)

    def post(self, request, format=None):
        from systems.commands.webhook import WebhookCommand

        def processor():
            options = self._format_options(request.data)
            command = type(self.command)(self.command.name, self.command.parent_instance).bootstrap(options)
            command.set_headers(request.headers)

            if isinstance(command, WebhookCommand):
                response = HttpResponse(
                    content=command.handle_api(options), status=200, content_type=command.get_response_type()
                )
            else:
                response = StreamingHttpResponse(
                    streaming_content=command.handle_api(options, package=True), content_type="application/json"
                )
            response["Cache-Control"] = "no-cache"
            return response

        def error_handler(error):
            return str(error)

        return wrap_api_call("command", request, processor, message=error_handler, api_type="command_api")

    def _format_options(self, options):
        if self.command.active_user:
            cipher = Cipher.get("command_api", user=self.command.active_user.name)

            def process_item(key, value):
                return (key, normalize_value(cipher.decrypt(value)))

            return self.command.format_fields(options, process_item)
        return self.command.format_fields(options)
