from rest_framework import serializers

from .models import *



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

class YesWorkflowSaveSerializer(serializers.Serializer):
    username = serializers.StringRelatedField()
    title = serializers.CharField(required=False, allow_blank=True, max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    model = serializers.CharField(required=False, allow_blank=False)
    model_checksum = serializers.CharField(required=False, allow_blank=True, max_length=128)
    graph = serializers.CharField(required=False, allow_blank=False)
    recon = serializers.CharField(required=False, allow_blank=True)
    tag = TagSerializer(required=False, many=True)

    # tags = serializers.ListField(
    #     child=serializers.CharField(required=False, allow_blank=True, max_length=32)
    # )
    # scripts = serializers.ListField(
    #     child=serializers.CharField(required=False, allow_blank=True, max_length=32)
    # )

    def create(self, validated_data):
        w = Workflow(
            user=validated_data.pop('username'),
            title=validated_data.pop('title'),
            description=validated_data.pop('description')
        )
        w.save()
        v = Version(
            workflow=w,

        )
        # w.save()

        # vs = VersionSerializer(JSONParser().parse(request))
        v = Version(
            workflow=w,
            yw_model_check_sum=request.data.get('model_checksum', ''),
            yw_model_output=request.data.get('model', ''),
            yw_graph_output=request.data.get('graph', ''),
            last_modified=datetime.datetime.now(tz=timezone.utc)
        )
        # v.save()
        # r = Run(
        #     version=v,
        #     yw_recon_output=request.data.get('recon', ''),
        #     run_time_stamp=datetime.datetime.now(tz=timezone.utc)
        # )
