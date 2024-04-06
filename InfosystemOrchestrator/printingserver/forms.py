from django import forms

from printingserver.models import StoredDocument


class UploadForm(forms.ModelForm):
    description = forms.CharField(label="Document description", max_length=100)
    file_to_print = forms.FileField(label="File to upload. Please do PDF")

    class Meta:
        model = StoredDocument
        fields = ['description', 'file_to_print', 'number_of_pages', 'priority', 'delivery_location']
