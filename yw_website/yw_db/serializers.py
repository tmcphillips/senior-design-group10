from rest_framework import serializers
from yw_db.models import Tag, Workflow, Version, Run, File, RunFile
# TODO: Do we need to serialize users? probably
# from django.contrib.auth.models import User

class TagSerializer(serializers.ModelSerializer):
    parent_tag = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Tag 
        fields = ('parent_tag', 'title', 'tag_type')

class WorkflowSerializer(serializers.ModelSerializer):
    users = serializers.RelatedField(read_only=True)
    class Meta:
        model = Workflow
        fields = ('users', 'title', 'description')

class VersionSerializer(serializers.ModelSerializer):
    workflows = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Version
        fields = ('script_check_sum', 'yw_model_check_sum', 'yw_model_output', 'yw_graph_output', 'last_modified')

class RunSerializer(serializers.ModelSerializer):
    versions = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Run
        fields = ('run_time_stamp', 'yw_recon_output')

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file_checksum', 'input_data', 'file_size', 'last_modified_time_stamp')

class RunFileSerializer(serializers.ModelSerializer):
    run_file = serializers.PrimaryKeyRelatedField(read_only=True)
    file_run = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = RunFile 
        fields = ('uri', 'file_name')

class TagWorkflowSerializer(serializers.ModelSerializer):
    tags_workflows = serializers.PrimaryKeyRelatedField(read_only=True)
    workflows_tags = serializers.PrimaryKeyRelatedField(read_only=True)

class TagVersionSerializer(serializers.ModelSerializer):
    tags_version = serializers.PrimaryKeyRelatedField(read_only=True)
    versions_tags = serializers.PrimaryKeyRelatedField(read_only=True)

class TagRunSerializer(serializers.ModelSerializer):
    tags_runs = serializers.PrimaryKeyRelatedField(read_only=True)
    runs_tags = serializers.PrimaryKeyRelatedField(read_only=True)

class TagFileSerializer(serializers.ModelSerializer):
    tags_files = serializers.PrimaryKeyRelatedField(read_only=True)
    files_tags = serializers.PrimaryKeyRelatedField(read_only=True)
