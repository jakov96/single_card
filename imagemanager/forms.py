from django.forms import ModelForm
from imagemanager.models import BaseImage


class BaseImageForm(ModelForm):
    class Meta:
        model = BaseImage
        fields = ['original']
