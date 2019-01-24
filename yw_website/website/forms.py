from django import forms
from django.contrib.auth.forms import UserCreationForm, ModelForm
from django.contrib.auth.models import User
from yw_db.models import *

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


class VersionSelectionForm(ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
