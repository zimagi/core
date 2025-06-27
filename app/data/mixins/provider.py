from systems.models.index import ModelMixin, ModelMixinFacade
from systems.models.errors import ProviderError


class ProviderMixinFacade(ModelMixinFacade("provider")):
    @property
    def provider_name(self):
        if getattr(self.meta, "provider_name", None):
            return self.meta.provider_name
        return None


class ProviderMixin(ModelMixin("provider")):
    def initialize(self, command, facade=None, **options):
        if not super().initialize(command, **options):
            return False

        if self.facade.provider_name:
            self._provider = command.get_provider(
                self.facade.provider_name, self.provider_type, instance=self, facade=facade
            )
        return True

    @property
    def provider(self):
        if not getattr(self, "_provider", None):
            if self.manager.active_command and self.facade.provider_name:
                self._provider = self.manager.active_command.get_provider(
                    self.facade.provider_name, self.provider_type, instance=self
                )
        if not getattr(self, "_provider", None):
            raise ProviderError("Provider has not been initialized.  Please run: instance.initialize(command)")
        return self._provider
