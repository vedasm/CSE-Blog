from pathlib import PurePosixPath

from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.core.files.utils import validate_file_name
from django.utils.text import get_valid_filename


class DatabaseStorage(Storage):
    """Store uploaded files in PostgreSQL instead of Render's ephemeral disk."""

    def _normalize_name(self, name):
        normalized = str(PurePosixPath(name)).lstrip('/')
        validate_file_name(normalized, allow_relative_path=True)
        return normalized

    def _open(self, name, mode='rb'):
        from apps.core.models import StoredFile

        if mode != 'rb':
            raise ValueError('DatabaseStorage only supports binary reads.')
        stored = StoredFile.objects.get(name=self._normalize_name(name))
        return ContentFile(bytes(stored.content), name=stored.name)

    def _save(self, name, content):
        from apps.core.models import StoredFile

        name = self._normalize_name(name)
        data = b''.join(content.chunks())
        StoredFile.objects.update_or_create(
            name=name,
            defaults={
                'content': data,
                'content_type': getattr(content, 'content_type', ''),
                'size': len(data),
            },
        )
        return name

    def delete(self, name):
        from apps.core.models import StoredFile

        StoredFile.objects.filter(name=self._normalize_name(name)).delete()

    def exists(self, name):
        from apps.core.models import StoredFile

        return StoredFile.objects.filter(name=self._normalize_name(name)).exists()

    def size(self, name):
        from apps.core.models import StoredFile

        return StoredFile.objects.only('size').get(name=self._normalize_name(name)).size

    def url(self, name):
        return f'/media/{self._normalize_name(name)}'

    def get_valid_name(self, name):
        return get_valid_filename(name)
