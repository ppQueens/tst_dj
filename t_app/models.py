from django.db import models


class SomeModel(models.Model):
    file = models.FileField(upload_to='files')

    def __str__(self):
        return self.file.name.split('/')[-1]

    def file_size(self):
        return f'{round(self.file.size / 1024 / 1024, 7)} MB'
