from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class NoAutofocusPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.pop('autofocus', None)
