from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from yw_db.models import Workflow


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')
    email = forms.EmailField(max_length=254, required=False)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

# added
class VersionsForm(forms.Form):
    # Will need to change from docuements to versions when ready
    versions = forms.ModelChoiceField(queryset=Workflow.objects.all(), required = False, empty_label="Version 1")
