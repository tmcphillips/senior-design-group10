import datetime
from haystack import indexes
from .models import Workflow


class WorkflowIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Workflow

