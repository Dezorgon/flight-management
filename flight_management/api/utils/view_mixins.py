from typing import Any

from django.core.exceptions import ImproperlyConfigured


class GetSerializerMixin:
    serializer_classes: dict[str, Any] = None

    def get_serializer_class(self):
        if self.serializer_classes is None:
            raise ImproperlyConfigured('Field serializer_classes must be declared')

        serializer = self.serializer_classes.get(self.action, None)

        if serializer is None:
            if 'default' not in self.serializer_classes:
                raise KeyError('Key default must be in serializer_class')
            serializer = self.serializer_classes['default']

        return serializer
