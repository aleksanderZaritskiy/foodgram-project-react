from django.forms import ModelForm

from .models import ImportFile


class ImportFileForm(ModelForm):
    class Meta:
        model = ImportFile
        fields = ('file',)
