from django import forms
from haystack.forms import SearchForm, ModelSearchForm
from .models import Workflow, Version, Tag, Run, Script, File

class WorkflowSearchForm(SearchForm):
    def no_query_found(self):
        return Workflow.objects.all().exclude(version__isnull=True)
