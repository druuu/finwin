from django import forms
from app.models import *


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(UserForm, self).save(commit=False)
        if commit:
            instance.save()
        if self.cleaned_data.get("password"):
            instance.set_password(self.cleaned_data.get("password"))
            instance.save()

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not (self.instance.id or password):
            raise forms.ValidationError("Please provide password")
        return password

    class Meta:
        model = User
        fields = ("email", "username", "password")

