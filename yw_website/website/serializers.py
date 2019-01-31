from rest_framework import serializers
from website.models import *

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag 
        fields = '__all__'

class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = '__all__'

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class RunFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunFile 
        fields = '__all__'

class TagWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagWorkflow
        fields = '__all__'

class TagVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagVersion
        fields = '__all__'

class TagRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagRun
        fields = '__all__'


class TagFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagFile
        fields = '__all__'
