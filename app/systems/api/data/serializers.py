import copy
from collections.abc import Mapping

from rest_framework import fields
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer, Serializer, SerializerMethodField
from systems.commands import action
from systems.models import fields as zimagi_fields
from utility.data import ensure_list, normalize_value

from .fields import HyperlinkedRelatedField, JSONDataField


def get_field_map(facade, fields=None, api_url=True, id=True, dynamic=True, short=True):
    def get_dynamic_field(field_name):
        def _dynamic_display(self, instance):
            instance = copy.deepcopy(instance)
            instance.initialize(self.command)

            value = getattr(instance, field_name, None)
            if "<locals>.RelatedManager" in str(type(value)):
                value = None

            display_function = getattr(facade, f"get_field_{field_name}_display", None)
            if display_function:
                value = facade.raw_text(display_function(instance, value, short))
            return value

        return _dynamic_display

    if fields is None:
        fields = list(set(facade.atomic_fields) - set(facade.dynamic_fields))
    if not id:
        fields.remove(facade.pk)

    field_map = {
        "Meta": type(
            "Meta",
            (object,),
            {"model": facade.model, "fields": [field for field in fields if field not in facade.hidden_fields()]},
        )
    }
    if api_url or "api_url" in fields:
        field_map["api_url"] = HyperlinkedIdentityField(view_name=f"{facade.name}-detail", lookup_field=facade.pk)
        field_map["Meta"].fields.append("api_url")
    if dynamic:
        for field_name in facade.dynamic_fields:
            field_map[field_name] = SerializerMethodField()
            field_map[f"get_{field_name}"] = get_dynamic_field(field_name)
            field_map["Meta"].fields.append(field_name)

    return field_map


def get_related_field_map(facade, fields=None, api_url=True, id=True, dynamic=True, short=True, summary=True, reverse=False):
    item_serializer = SummarySerializer if summary else LinkSerializer
    field_map = get_field_map(facade, fields=fields, api_url=api_url, id=id, dynamic=dynamic, short=short)
    for field_name, info in facade.get_referenced_relations().items():
        if getattr(info["model"], "facade", None) and info["model"].facade.check_api_enabled():
            field_map[field_name] = item_serializer(info["model"].facade, False)(many=info["multiple"])
            field_map["Meta"].fields.append(field_name)

    if reverse:
        for field_name, info in facade.get_reverse_relations().items():
            if getattr(info["model"], "facade", None) and info["model"].facade.check_api_enabled():
                related_facade = info["model"].facade
                related_field_name = facade.get_reverse_field(info)

                if related_field_name:
                    field_map[field_name] = HyperlinkedRelatedField(
                        related_facade, f"{related_facade.name}-list", f"{related_field_name}__{facade.pk}"
                    )
                    field_map["Meta"].fields.append(field_name)

    return field_map


class BaseSerializer(Serializer):
    def __init__(self, *args, command=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = command


class BaseModelSerializer(ModelSerializer):
    def __init__(self, *args, command=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = command


class BaseItemSerializer(HyperlinkedModelSerializer):
    def __init__(self, *args, command=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = command

        self.serializer_field_mapping[zimagi_fields.DataField] = JSONDataField

    @property
    def view(self):
        return self._context.get("view", None)

    @property
    def view_request(self):
        return self._context.get("request", None)

    @property
    def view_format(self):
        return self._context.get("format", None)


def LinkSerializer(facade, dynamic=False):
    class_name = "{}LinkSerializer".format(facade.name.title().replace("_", ""))

    if class_name in globals():
        return globals()[class_name]

    serializer = type(
        class_name,
        (BaseItemSerializer,),
        get_field_map(
            facade,
            fields=[facade.pk, facade.key()] if facade.pk != facade.key() else [facade.pk],
            api_url=True,
            id=True,
            dynamic=dynamic,
            short=True,
        ),
    )
    globals()[class_name] = serializer
    return serializer


def SummarySerializer(facade, dynamic=True):
    class_name = "{}SummarySerializer".format(facade.name.title().replace("_", ""))

    if class_name in globals():
        return globals()[class_name]

    serializer = type(
        class_name,
        (BaseItemSerializer,),
        get_related_field_map(facade, api_url=True, id=True, dynamic=dynamic, short=True, summary=False, reverse=False),
    )
    globals()[class_name] = serializer
    return serializer


def DetailSerializer(facade):
    class_name = "{}DetailSerializer".format(facade.name.title().replace("_", ""))

    if class_name in globals():
        return globals()[class_name]

    serializer = type(
        class_name,
        (BaseItemSerializer,),
        get_related_field_map(facade, api_url=False, id=True, dynamic=True, short=False, summary=True, reverse=True),
    )
    globals()[class_name] = serializer
    return serializer


class ValuesSerializer(BaseSerializer):
    count = fields.IntegerField(min_value=0)
    results = fields.ListField(allow_empty=True)


class CountSerializer(BaseSerializer):
    count = fields.IntegerField(min_value=0)


def check_data_overlap(data_types):
    if len(data_types) <= 2:
        return False
    if len(data_types) != len(set(data_types)):
        return True
    return False


def get_update_field_map(facade, exclude_fields, parent_data):
    field_index = facade.field_index
    editable_fields = [field.name for field in facade.editable_field_instances]
    fields = list(set(facade.atomic_fields) - set(facade.dynamic_fields))
    extra_kwargs = {}

    meta_fields = []
    for field_name in fields:
        if field_name in editable_fields and field_name not in exclude_fields:
            meta_fields.append(field_name)

            field = field_index[field_name]
            if field.blank or field.null:
                extra_kwargs[field_name] = {"allow_null": True}

    field_map = {
        "Meta": type("Meta", (object,), {"model": facade.model, "fields": meta_fields, "extra_kwargs": extra_kwargs})
    }
    for field_name, info in facade.get_referenced_relations().items():
        if getattr(info["model"], "facade", None) and field_name not in exclude_fields:
            if not check_data_overlap([*parent_data, info["model"].facade.name]):
                relation_field = info["field"]
                required = True
                nullable = False

                if relation_field.has_default() or relation_field.blank or relation_field.null:
                    required = False
                    if relation_field.blank or relation_field.null:
                        nullable = True

                field_map["Meta"].fields.append(field_name)
                field_map[field_name] = UpdateSerializer(
                    info["model"].facade, parent_data=[*parent_data, info["model"].facade.name]
                )(many=info["multiple"], required=required, allow_null=nullable)

    for field_name, info in facade.get_reverse_relations().items():
        if getattr(info["model"], "facade", None) and field_name not in exclude_fields:
            if not check_data_overlap([*parent_data, info["model"].facade.name]):
                related_field_name = facade.get_reverse_field(info)

                if related_field_name:
                    field_map["Meta"].fields.append(field_name)
                    field_map[field_name] = UpdateSerializer(
                        info["model"].facade,
                        parent_data=[*parent_data, info["model"].facade.name],
                        exclude_fields=[related_field_name],
                    )(many=True, required=False)

    return field_map


def save_relation(command, facade, field_name, data):
    if isinstance(data, dict):
        facade = copy.deepcopy(facade)
        scope_fields = facade.scope_parents
        instance = None

        if facade.key() not in data and facade.pk not in data:
            raise Exception(f"Relation {field_name} data requires key field {facade.key()} or id field {facade.pk}")

        if facade.pk in data:
            instance = facade.retrieve_by_id(data[facade.pk])
        else:
            facade.set_scope({key: item for key, item in data.items() if key in scope_fields})
            instance = facade.retrieve(data[facade.key()])

        sub_command = action.child(command, facade.name, data)
        success = True
        try:
            serializer = UpdateSerializer(facade)(instance=instance, data=data, partial=True, command=sub_command)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

        except Exception as e:
            sub_command.error(e, terminate=False)
            success = False
            raise e
        finally:
            sub_command.log_status(success)

        data = getattr(instance, facade.pk)

    return data


def save_reverse_relations(command, facade, instance, data):
    reverse_index = facade.get_reverse_relations()

    for field_name, values in data.items():
        field_info = reverse_index[field_name]
        related_facade = field_info["model"].facade
        related_field = facade.get_reverse_field(field_info)

        if related_field:
            for reverse_fields in ensure_list(values):
                if field_info["multiple"]:
                    reverse_fields[related_field] = [f"+{instance.pk}"]
                else:
                    reverse_fields[related_field] = instance.pk

                save_relation(command, related_facade, field_name, reverse_fields)


def get_scope_ids(command, facade, scope_data):
    relation_index = facade.get_referenced_relations()
    scope_values = {}

    for field_name, data in scope_data.items():
        index_field = field_name.removesuffix("_id")
        field_id = f"{index_field}_id"
        scope_facade = relation_index[index_field]["model"].facade

        scope_values[field_id] = save_relation(command, scope_facade, field_name, data)
    return scope_values


def get_relation_ids(command, facade, relation_data):
    relation_index = facade.get_extra_relations()
    relation_values = {}

    for field_name, data in relation_data.items():
        index_field = field_name.removesuffix("_id")
        relation_info = relation_index[index_field]
        relation_facade = relation_info["model"].facade

        if relation_info["multiple"]:
            if index_field not in relation_values:
                relation_values[index_field] = []

            for relation in data:
                relation_values[index_field].append(save_relation(command, relation_facade, field_name, relation))
        else:
            relation_values[f"{index_field}_id"] = save_relation(command, relation_facade, field_name, data)
    return relation_values


def UpdateSerializer(facade, exclude_fields=None, parent_data=None):
    class_name = "{}UpdateSerializer".format(facade.name.title().replace("_", ""))

    if exclude_fields is None:
        exclude_fields = []
    if parent_data is None:
        parent_data = []

    def to_internal_value(self, data):
        if not isinstance(data, Mapping):
            return normalize_value(data)
        return super(BaseModelSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        scope, fields, relations, reverse = facade.split_field_values(validated_data)

        instance = self.command.save_instance(
            facade,
            validated_data.pop(facade.key()),
            fields={
                **get_relation_ids(self.command, facade, relations),
                **get_scope_ids(self.command, facade, scope),
                **fields,
            },
        )
        if reverse:
            save_reverse_relations(self.command, facade, instance, reverse)
        return instance

    def update(self, instance, validated_data):
        scope, fields, relations, reverse = facade.split_field_values(validated_data)

        provider_type = None
        if getattr(instance, "provider_type", None):
            provider_type = validated_data.pop("provider_type", instance.provider_type)

        instance = self.command.save_instance(
            facade,
            getattr(instance, facade.key()),
            fields={
                **get_relation_ids(self.command, facade, relations),
                **get_scope_ids(self.command, facade, scope),
                **fields,
                "provider_type": provider_type,
            },
        )
        if reverse:
            save_reverse_relations(self.command, facade, instance, reverse)
        return instance

    return type(
        class_name,
        (BaseModelSerializer,),
        {
            **get_update_field_map(facade, exclude_fields, [*parent_data, facade.name]),
            "to_internal_value": to_internal_value,
            "create": create,
            "update": update,
        },
    )
