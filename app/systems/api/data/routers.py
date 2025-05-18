from functools import lru_cache

from django.conf import settings
from django.urls import re_path
from rest_framework import routers


class DataAPIRouter(routers.SimpleRouter):
    routes = [
        # List route
        routers.Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={"get": "list", "post": "create"},
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
        # CSV route
        routers.Route(
            url=r"^{prefix}/csv{trailing_slash}$",
            mapping={"get": "csv"},
            name="{basename}-csv",
            detail=False,
            initkwargs={"suffix": "CSV"},
        ),
        # JSON route
        routers.Route(
            url=r"^{prefix}/json{trailing_slash}$",
            mapping={"get": "json"},
            name="{basename}-csv",
            detail=False,
            initkwargs={"suffix": "JSON"},
        ),
        # Values route
        routers.Route(
            url=r"^{prefix}/values/{field_lookup}{trailing_slash}$",
            mapping={"get": "values"},
            name="{basename}-values",
            detail=False,
            initkwargs={"suffix": "Values"},
        ),
        # Count route
        routers.Route(
            url=r"^{prefix}/count/{field_lookup}{trailing_slash}$",
            mapping={"get": "count"},
            name="{basename}-count",
            detail=False,
            initkwargs={"suffix": "Count"},
        ),
        # Detail route
        routers.Route(
            url=r"^{prefix}/{lookup}{trailing_slash}$",
            mapping={"get": "retrieve", "put": "update", "delete": "destroy"},
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Instance"},
        ),
    ]

    def __init__(self):
        self.trailing_slash = "/?"
        super().__init__()

    def get_field_lookup_regex(self, viewset, lookup_prefix=""):
        base_regex = "(?P<{lookup_prefix}field_lookup>{lookup_value})"
        lookup_value = getattr(viewset, "lookup_value_regex", "[^/.]+")

        return base_regex.format(lookup_prefix=lookup_prefix, lookup_value=lookup_value)

    def get_default_basename(self, viewset):
        return viewset.facade.name

    @lru_cache(maxsize=None)
    def get_urls(self):
        urls = []

        for name, facade in settings.MANAGER.index.get_facade_index().items():
            if facade.check_api_enabled():
                self.register(facade.name, facade.get_viewset())

        for prefix, viewset, basename in self.registry:
            lookup = self.get_lookup_regex(viewset)
            field_lookup = self.get_field_lookup_regex(viewset)
            routes = self.get_routes(viewset)
            disabled_ops = viewset.facade.disabled_ops()

            for route in routes:
                mapping = self.get_method_map(viewset, route.mapping)
                if not mapping:
                    continue

                if disabled_ops:
                    for method in list(mapping.keys()):
                        operation = mapping[method]

                        if operation in disabled_ops:
                            mapping.pop(method)
                        elif operation == "create" and "update" in disabled_ops:
                            mapping.pop(method)
                        elif operation != "retrieve" and method == "get" and "list" in disabled_ops:
                            mapping.pop(method)

                regex = route.url.format(
                    prefix=prefix, lookup=lookup, field_lookup=field_lookup, trailing_slash=self.trailing_slash
                )

                if not prefix and regex[:2] == "^/":
                    regex = "^" + regex[2:]

                initkwargs = route.initkwargs.copy()
                initkwargs.update({"basename": basename, "detail": route.detail})
                view = viewset.as_view(mapping, **initkwargs)
                name = route.name.format(basename=basename)
                urls.append(re_path(regex, view, name=name))

        return urls
