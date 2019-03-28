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

class ProgramBlockIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    qualified_name = indexes.CharField(model_attr="qualified_name")

    def get_model(self):
        return ProgramBlock


class DataIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    qualified_name = indexes.CharField(model_attr="qualified_name")

    def get_model(self):
        return Data


class PortIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    qualified_name = indexes.CharField(model_attr="qualified_name")
    alias = indexes.CharField(model_attr="alias")
    uri_template = indexes.CharField(model_attr="uri_template")

    def get_model(self):
        return Port

class UriVariableIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")

    def get_model(self):
        return UriVariable

class ResourceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    uri = indexes.CharField(model_attr="uri")
    checksum = indexes.CharField(model_attr="checksum")

    def get_model(self):
        return Resource

class UriVariableValueIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    value = indexes.CharField(model_attr="value")

    def get_model(self):
        return UriVariableValue