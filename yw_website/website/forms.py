from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from yw_db.models import Version


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(
        max_length=30, required=True, help_text='Required')
    email = forms.EmailField(max_length=254, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )


class VersionsForm(forms.Form):
    class Meta:
        model = Version
    versions = forms.ModelChoiceField(
        queryset=Version.objects.all(), required=False, empty_label="Version 1")

    def __init__(self, workflow, *args, **kwargs):
        super(VersionsForm, self).__init__(*args, **kwargs)
        self.queryset = Version.objects.all().filter(workflow=workflow)
