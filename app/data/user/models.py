import binascii
import os

from django.conf import settings
from django.contrib.auth import base_user
from django.contrib.auth.base_user import BaseUserManager
from settings.roles import Roles
from systems.encryption.cipher import Cipher
from systems.models.index import DerivedAbstractModel, Model, ModelFacade


class UserFacade(ModelFacade("user")):
    def ensure(self, command, reinit, force):
        admin = self.retrieve(settings.ADMIN_USER)
        if not admin:
            admin = command.user_provider.create(settings.ADMIN_USER, {})

        self.manager.runtime.admin_user(admin)

        for name, config in settings.MANAGER.index.users.items():
            user = self.retrieve(name)
            if not user:
                command.user_provider.create(name, config, quiet=True)
            else:
                user.provider.update(config, quiet=True)

    def keep(self, key=None):
        return [settings.ADMIN_USER] + list(settings.MANAGER.index.users.keys())

    def keep_relations(self):
        keep_relations = {"groups": {settings.ADMIN_USER: Roles.admin}}

        for name, config in settings.MANAGER.index.users.items():
            if config.get("groups", None):
                keep_relations["groups"][name] = config["groups"]

        return keep_relations

    @property
    def admin(self):
        return self.manager.runtime.admin_user()

    @property
    def active_user(self):
        if not self.manager.runtime.active_user():
            self.set_active_user(self.admin)
        return self.manager.runtime.active_user()

    def set_active_user(self, user):
        self.manager.runtime.active_user(user)

    def generate_token(self, size=40):
        return binascii.hexlify(os.urandom(size)).decode()[:size]


class UserManager(BaseUserManager):
    use_in_migrations = True


class User(Model("user"), DerivedAbstractModel(base_user, "AbstractBaseUser", "password", "last_login")):
    USERNAME_FIELD = "name"

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.password and self.name == settings.ADMIN_USER:
            self.set_password(settings.DEFAULT_ADMIN_TOKEN)

        if not self.encryption_key or self.encryption_key == "<generate>":
            self.encryption_key = Cipher.get_provider_class("user_api_key").generate_key()

        super().save(*args, **kwargs)

    def get_language_model(self, command, reset=False):
        if (reset or not getattr(self, "_language_model", None)) and self.language_provider:
            self._language_model = command.get_provider(
                "language_model", self.language_provider, **self.language_provider_options
            )
        return self._language_model

    def get_text_splitter(self, command, reset=False):
        if (reset or not getattr(self, "_text_splitter", None)) and self.text_splitter_provider:
            self._text_splitter = command.get_provider(
                "text_splitter", self.text_splitter_provider, **self.text_splitter_provider_options
            )
        return self._text_splitter

    def get_encoder(self, command, reset=False):
        if (reset or not getattr(self, "_encoder", None)) and self.encoder_provider:
            self._encoder = command.get_provider("encoder", self.encoder_provider, **self.encoder_provider_options)
        return self._encoder

    def get_qdrant_collection(self, command, name, reset=False, **options):
        if not getattr(self, "_qdrant_collection", None):
            self._qdrant_collection = {}

        if reset or name not in self._qdrant_collection:
            encoder = self.get_encoder(command, reset=reset)
            self._qdrant_collection[name] = command.get_provider(
                "qdrant_collection", name, dimension=encoder.field_dimension, **options
            )
        return self._qdrant_collection[name]

    def get_search_limit(self, override=None):
        return override if override else self.search_limit

    def get_search_min_score(self, override=None):
        return override if override else self.search_min_score
