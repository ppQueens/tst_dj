import pathlib, ffmpy, uuid, os

from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib import admin

from .models import SomeModel

# todo move to settings
two_and_half_megabytes = 2621440
path_to_default_file = '/home/user/Downloads/SampleVideo_1280x720_1mb.mp4'


@admin.register(SomeModel)
class SomeModelAdmin(admin.ModelAdmin):
    list_display = 'file', 'file_size'
    readonly_fields = 'file_size',

    def save_model(self, request, obj, form, change):
        ext = pathlib.Path(obj.file.url).suffix
        file_name = uuid.uuid4().hex
        new_file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        if ext == '.mp4' and obj.file.size > two_and_half_megabytes:
            ff = ffmpy.FFmpeg(
                inputs={obj.file.url: None},
                outputs={f'{new_file_path}.gif': None})
            ff.run()
        elif ext != '.mp4':
            with open(path_to_default_file, 'rb') as f:
                obj.file = ContentFile(f.read(), f'{file_name}.mp4')
        else:
            obj.file.name = f'{file_name}{ext}'
        super().save_model(request, obj, form, change)
