from systems.models.index import Model, ModelFacade

import zimagi


class HostFacade(ModelFacade("host")):
    def get_field_token_display(self, instance, value, short):
        if value and short:
            return super().get_field_token_display(instance, value[:10] + "...", short)
        return super().get_field_token_display(instance, value, short)

    def get_field_encryption_key_display(self, instance, value, short):
        if value and short:
            return super().get_field_encryption_key_display(instance, value[:10] + "...", short)
        return super().get_field_encryption_key_display(instance, value, short)


class Host(Model("host")):
    def command_api(self, options_callback=None, message_callback=None):
        port = self.command_port
        client = None

        if port:
            client = zimagi.CommandClient(
                user=self.user,
                token=self.token,
                encryption_key=self.encryption_key,
                host=self.host,
                port=port,
                options_callback=options_callback,
                message_callback=message_callback,
            )
        return client

    def data_api(self, options_callback=None):
        port = self.data_port
        client = None

        if port:
            client = zimagi.DataClient(
                user=self.user,
                token=self.token,
                encryption_key=self.encryption_key,
                host=self.host,
                port=port,
                options_callback=options_callback,
            )
        return client
