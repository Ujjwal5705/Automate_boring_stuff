
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Email


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ("__all__")
        widgets = {
            'message': CKEditorWidget(),
        }