from rest_framework import serializers
from yw_db.models import *

class TagSerializer(serializers.ModelSerializer):
    parent_tag = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Tag 
        fields = ('parent_tag', 'title', 'tag_type')

class WorkflowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Workflow
        fields = ('user', 'title', 'description')

class VersionSerializer(serializers.ModelSerializer):
    workflow = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Version
        fields = ('workflow', 'script_check_sum', 'yw_model_check_sum', 'yw_model_output', 'yw_graph_output', 'last_modified')

class RunSerializer(serializers.ModelSerializer):
    version = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Run
        fields = ('version', 'run_time_stamp', 'yw_recon_output')

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file_checksum', 'input_data', 'file_size', 'last_modified')

class RunFileSerializer(serializers.ModelSerializer):
    run = serializers.PrimaryKeyRelatedField(read_only=True)
    file = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = RunFile 
        fields = ('run', 'file', 'uri', 'file_name')

class TagWorkflowSerializer(serializers.ModelSerializer):
    tag = serializers.PrimaryKeyRelatedField(read_only=True)
    workflow = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = TagWorkflow
        fields = ('tag', 'workflow')

class TagVersionSerializer(serializers.ModelSerializer):
    tag = serializers.PrimaryKeyRelatedField(read_only=True)
    version = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = TagVersion
        fields = ('tag', 'version')

class TagRunSerializer(serializers.ModelSerializer):
    tag = serializers.PrimaryKeyRelatedField(read_only=True)
    run = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = TagRun
        fields = ('tag', 'run')

class TagFileSerializer(serializers.ModelSerializer):
    tag = serializers.PrimaryKeyRelatedField(read_only=True)
    file = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = TagFile
        fields = ('tag', 'file')
