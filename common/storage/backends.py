from django.conf import settings
from django.core.files.storage import FileSystemStorage


class PublicMediaStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        location = kwargs.pop("location", settings.MEDIA_ROOT)
        base_url = kwargs.pop("base_url", settings.MEDIA_URL)
        super().__init__(location=location, base_url=base_url, *args, **kwargs)
