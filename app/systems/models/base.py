import copy
import importlib
import logging
import time

from django.conf import settings
from django.db import models as django
from django.db.models.base import ModelBase
from django.db.transaction import atomic
from django.utils.timezone import now
from utility.mutex import MutexError, MutexTimeoutError, check_mutex

from .facade import ModelFacade
from .index import check_dynamic, get_dynamic_class_name, get_facade_class_name, get_spec_key, get_stored_class_name

logger = logging.getLogger(__name__)


django.options.DEFAULT_NAMES += ("data_name", "scope", "dynamic_fields", "provider_name", "command_base")


def format_field_choices(choices):
    choice_list = []
    if isinstance(choices, (list, tuple)):
        for choice in choices:
            if isinstance(choice, (list, tuple)):
                choice_list.append(tuple(choice))
            else:
                choice_list.append((choice, choice))
    else:
        for value, label in choices.items():
            choice_list.append((value, label))
    return choice_list


def model_index():
    return settings.MANAGER.index


def classify_parents(parent_classes):
    map = {}
    for parent in parent_classes:
        try:
            key = get_spec_key(parent.__module__)
        except Exception as e:
            key = "base"

        map.setdefault(key, [])
        map[key].append(parent)
    return map


def classify_model(model_class_name):
    module_name = model_index().model_class_path.get(model_class_name, None)
    if module_name:
        return get_spec_key(module_name)
    return "unknown"


def run_transaction(facade, transaction_id, callback):
    transaction_id = f"model-transaction-{facade.name}-{transaction_id}"
    while True:
        try:
            with check_mutex(transaction_id):
                with atomic():
                    callback()
                    break

        except (MutexError, MutexTimeoutError) as error:
            logger.debug(f"Failed to acquire transaction lock {transaction_id}: {error}")

        time.sleep(0.1)


class DatabaseAccessError(Exception):
    pass


class FacadeNotExistsError(Exception):
    pass


class BaseModelMixin(django.Model):
    created = django.DateTimeField(null=True, editable=False)
    updated = django.DateTimeField(null=True, editable=False)

    class Meta:
        abstract = True

    def initialize(self, command, **options):
        return True

    def save(self, *args, **kwargs):
        if self.created is None:
            self.created = now()
        self.updated = now()

        super().save(*args, **kwargs)

    @property
    def manager(self):
        return settings.MANAGER

    @property
    def facade(self):
        return self.__class__.facade

    @property
    def facade_clone(self):
        return copy.deepcopy(self.facade)

    @property
    def new_facade(self):
        return self.__class__.new_facade

    def run_transaction(self, transaction_id, callback):
        return run_transaction(self.facade, transaction_id, callback)

    def parse_fields(self, *excluded_fields):
        def parse(instance, recurse=False):
            fields = {"_type": instance.facade.meta.data_name}

            # Basic fields
            for field in list(set(instance.facade.fields) - set(excluded_fields)):
                fields[field] = getattr(instance, field, None)

            # Referenced Relation fields
            for field_name, field_info in instance.facade.get_referenced_relations().items():
                if recurse and field_name not in excluded_fields:
                    related_field = getattr(instance, field_name)

                    if related_field:
                        if field_info["multiple"]:
                            fields[field_name] = [parse(item) for item in related_field.all()]
                        else:
                            fields[field_name] = parse(related_field)

            # Reverse Relation fields
            for field_name, field_info in instance.facade.get_reverse_relations().items():
                if recurse and field_name not in excluded_fields:
                    fields[field_name] = []

                    for relation in getattr(instance, field_name).all():
                        fields[field_name].append(parse(relation))

            return fields

        return parse(self, recurse=True)


class BaseMetaModel(ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        spec_key = classify_model(name)
        parent_map = classify_parents(bases)
        meta_info = attrs.get("_meta_info", {})
        meta_bases = []

        logger.info(f"++++ Creating new model: {name} <{spec_key}> {bases}")
        for field, value in meta_info.items():
            logger.debug(f" init meta > {field} - {value}")

        for key in ("data", "data_mixins", "data_base", "base"):
            for parent in parent_map.get(key, []):
                if key in ("base", "data_base"):
                    if getattr(parent, "Meta", None):
                        meta_bases.append(parent.Meta)

                for field, value in getattr(parent, "_meta_info", {}).items():
                    if field[0] != "_" and field not in ("abstract", "db_table"):
                        meta_info.setdefault(field, value)

        if spec_key == "data" and not check_dynamic(name):
            meta_info["abstract"] = False
        else:
            meta_info["abstract"] = True

        if not meta_info["abstract"]:
            spec = model_index().spec["data"][meta_info["data_name"]]
            app_name = spec.get("app", meta_info["data_name"])
            data_info = model_index().module_map["data"][app_name]
            meta_info["db_table"] = "{}_{}".format(data_info.module.replace("-", "_"), meta_info["data_name"])

        attrs["Meta"] = type("Meta", tuple(meta_bases), meta_info)

        for field in dir(attrs["Meta"]):
            if field[0] != "_":
                logger.debug(" final meta > {} - {}".format(field, getattr(attrs["Meta"], field)))

        return super().__new__(cls, name, bases, attrs, **kwargs)

    @property
    def facade_class(cls):
        class_name = get_stored_class_name(cls.__name__)
        facade_class_name = get_facade_class_name(class_name)
        dynamic_facade_class_name = get_dynamic_class_name(facade_class_name)

        module_name = model_index().model_class_path.get(class_name, None)
        module = importlib.import_module(module_name)

        if getattr(module, facade_class_name, None):
            facade_class = getattr(module, facade_class_name)
        elif getattr(module, dynamic_facade_class_name, None):
            facade_class = getattr(module, dynamic_facade_class_name)
        else:
            raise FacadeNotExistsError(f"Neither dynamic or coded facades exist for model {class_name}")
        return facade_class

    @property
    def facade(cls):
        facade = None
        if not cls._meta.abstract:
            facade = model_index().model_class_facades.get(cls.__name__, None)
            if not facade:
                facade = cls.new_facade
                model_index().model_class_facades[cls.__name__] = facade
        return facade

    @property
    def facade_clone(cls):
        return copy.deepcopy(cls.facade)

    @property
    def new_facade(cls):
        return cls.facade_class(cls)


class BaseMixin(django.Model, metaclass=BaseMetaModel):
    class Meta:
        abstract = True


class BaseModel(BaseModelMixin, metaclass=BaseMetaModel):
    class Meta:
        abstract = True
        facade_class = ModelFacade
