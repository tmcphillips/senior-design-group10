import datetime
from haystack import indexes
from .models import *


class WorkflowIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    def get_model(self):
        return Workflow

class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    def get_model(self):
        return Tag

class VersionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    yw_model_checksum = indexes.CharField(model_attr='yw_model_checksum')
    yw_model_output = indexes.CharField(model_attr='yw_model_output')
    yw_graph_output = indexes.CharField(model_attr='yw_graph_output')
    def get_model(self):
        return Version

class ScriptIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    checksum = indexes.CharField(model_attr='checksum')
    content = indexes.CharField(model_attr='content')
    def get_model(self):
        return Script

class RunIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    run_time_stamp = indexes.CharField(model_attr='run_time_stamp')
    yw_recon_output = indexes.CharField(model_attr='yw_recon_output')
    def get_model(self):
        return Run
