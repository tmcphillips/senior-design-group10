from django import forms
from django.contrib.auth.forms import UserCreationForm

from script_upload.models import Document
from django.contrib.auth.models import User

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', 'title', 'workflow')

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')
    email = forms.EmailField(max_length=254, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


# Used for images, doesn't work right now
class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

# added
class VersionsForm(forms.Form):
    # Will need to change from docuements to versions when ready
    versions = forms.ModelChoiceField(queryset=Document.objects.all(), required = False, empty_label="Version 1")

