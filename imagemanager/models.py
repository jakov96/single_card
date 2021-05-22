import os
from django.db import models
import PIL
from PIL import Image
from django.conf import settings


class BaseImage(models.Model):
    original = models.ImageField(verbose_name='Изображение', upload_to='images/%Y/%m/%d')
    image_min = models.CharField(max_length=250, default='', blank=True, editable=False)
    image_middle = models.CharField(max_length=250, default='', blank=True, editable=False)
    image_large = models.CharField(max_length=250, default='', blank=True, editable=False)
    alt = models.CharField(verbose_name='Тег alt', max_length=250, default='', blank=True)
    width = models.IntegerField(verbose_name='Ширина', null=True, blank=True)
    height = models.IntegerField(verbose_name='Высота', null=True, blank=True)

    IMAGE_MIN_WIDTH = 150
    IMAGE_MIDDLE_WIDTH = 450
    IMAGE_LARGE_WIDTH = 600

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def resize(self, new_width, modifier):
        path, filename = os.path.split(self.original.path)
        basename, extension = os.path.splitext(filename)
        file_name = os.path.join(path, '{0}{1}{2}'.format(basename, modifier, extension))

        image = Image.open(self.original.path)
        width = image.size[0]
        height = image.size[1]
        new_height = int(new_width * height / width)

        img = image.resize((new_width, new_height), PIL.Image.ANTIALIAS)
        img.save(file_name)

        path, filename = os.path.split(self.original.url)
        basename, extension = os.path.splitext(filename)
        file_name = os.path.join(path, '{0}{1}{2}'.format(basename, modifier, extension))

        return file_name.replace('\\', '/')

    def get_sizes(self):
        image = Image.open(self.original.path)
        width = image.size[0]
        height = image.size[1]
        return width, height

    def save(self, *args, **kwargs):
        try:
            old_obj = BaseImage.objects.get(id=self.id)
        except BaseImage.DoesNotExist:
            old_obj = None

        super(BaseImage, self).save(*args, **kwargs)

        if not self.width or not self.height:
            width, height = self.get_sizes()
            self.width = int(width)
            self.height = int(height)
            self.save()

        if not self.image_min or (old_obj and old_obj.original != self.original):
            self.image_min = self.resize(self.IMAGE_MIN_WIDTH, '-min')
            self.save()

        if not self.image_middle or (old_obj and old_obj.original != self.original):
            self.image_middle = self.resize(self.IMAGE_MIDDLE_WIDTH, '-middle')
            self.save()

        if not self.image_large or (old_obj and old_obj.original != self.original):
            self.image_large = self.resize(self.IMAGE_LARGE_WIDTH, '-large')
            self.save()

    def image_tag(self):
        return '<img src="%s" width="300"/>' % self.image_middle
    image_tag.allow_tags = True

    def min_image_tag(self):
        return '<img src="%s" width="40"/>' % self.image_min
    min_image_tag.allow_tags = True
    min_image_tag.short_description = 'Изображение'

    def to_json(self):
        return {
            'id': self.id,
            'original': self.original.url,
            'image_min': self.image_min,
            'image_middle': self.image_middle,
            'image_large': self.image_large,
            'alt': self.alt
        }

    def get_original_url(self):
        return settings.DOMAIN_URL + self.original.url

    def get_image_min_url(self):
        return settings.DOMAIN_URL + self.image_min

    def get_image_middle_url(self):
        return settings.DOMAIN_URL + self.image_middle

    def get_image_large_url(self):
        return settings.DOMAIN_URL + self.image_large
