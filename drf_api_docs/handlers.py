from collections import OrderedDict

from django.template.loader import render_to_string
from rest_framework import exceptions
from rest_framework.compat import coreapi, urlparse
from rest_framework.schemas import SchemaGenerator


def make_plain_schema(nested_schema) -> OrderedDict:
    """Makes plain ordered schema from nested schema recursively."""
    plain_schema = OrderedDict()

    def _unpack(schema, path=''):
        if hasattr(schema, 'data') and schema.data:
            for name, node in schema.data.items():
                new_path = '{} {}'.format(path, name) if path else name
                if hasattr(node, 'links') and node.links:
                    plain_schema[new_path] = node
                else:
                    _unpack(node, path=new_path)

    _unpack(nested_schema)
    return plain_schema


class CustomSchemaGenerator(SchemaGenerator):
    def get_link(self, path, method, view):
        methods = [
            'get_path_fields',
            'get_serializer_fields',
            'get_pagination_fields',
            'get_filter_fields'
        ]

        fields = []
        for method_name in methods:
            try:
                fields += getattr(self, method_name)(path, method, view)
            except (AttributeError, AssertionError):
                # it suppresses any exceptions caused by some custom serializers, methods etc.
                pass

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method, view)
        else:
            encoding = None

        description = self.get_description(path, method, view)

        if self.url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=urlparse.urljoin(self.url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=description
        )


class ApiDocsHandler(object):
    template = 'api_docs/template.md'

    def __init__(self, project_name: [str, None]=None, template: [str, None]=None):
        self.project_name = project_name or ''
        self.template = template or self.template

    def render(self) -> str:
        generator = CustomSchemaGenerator(
            title=self.project_name,
        )
        schema = generator.get_schema()

        if not schema:
            raise exceptions.ValidationError(
                'The schema generator did not return a schema Document'
            )

        return render_to_string(self.template, {
            'project_name': self.project_name,
            'api': make_plain_schema(schema)
        })
