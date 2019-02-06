from rest_framework import serializers

from .models import *
import datetime 


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')

class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        exclude = ('version',)

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

class YesWorkflowSaveSerializer(serializers.ModelSerializer):
    model = serializers.CharField(required=False, allow_blank=False)
    model_checksum = serializers.CharField(required=False, allow_blank=True, max_length=128)
    graph = serializers.CharField(required=False, allow_blank=False)
    recon = serializers.CharField(required=False, allow_blank=True)
    tags = serializers.ListField(
        child=serializers.CharField(required=False, allow_blank=True, max_length=32)
    )
    scripts = ScriptSerializer(many=True)
    files = FileSerializer(many=True)

    class Meta:
        model = Workflow
        fields =('title','description','model','model_checksum', 'graph', 'recon', 'tags', 'scripts', 'files' )


    def create(self, validated_data):
        w = Workflow(
            user=validated_data.get('username'),
            title=validated_data.get('title'),
            description=validated_data.get('description')
        )
        w.save()
        v = Version(
            workflow=w,
            yw_model_checksum=validated_data.get('model_checksum'),
            yw_model_output=validated_data.get('model'),
            yw_graph_output=validated_data.get('graph'),
            last_modified=datetime.datetime.now(tz=timezone.utc)
        )
        v.save()
        r = Run(
            version=v,
            run_time_stamp=datetime.datetime.now(tz=timezone.utc),
            yw_recon_output=validated_data.get('recon')
        )
        r.save()

        tags = TagSerializer(validated_data.get('tags'), many=True)
        for tag in tags.data:
            t = Tag(parent_tag=None, tag_type=Workflow, title=tag.get('title'))
            t.save()

        scripts = ScriptSerializer(validated_data.get('scripts'), many=True)
        for script in scripts.data:
            s = Script(name=script.get('name'), version=v, checksum=script.get('checksum'), content=script.get('content'))
            s.save()

        files = FileSerializer(validated_data.get('files'), many=True)
        for file in files.data:
            f = File(checksum=file.get('checksum'), size=file.get('size'), name=file.get('name'), uri=file.get('uri'), last_modified=file.get('last_modified'))
            f.save()

        return w.pk, v.pk, r.pk
    
    def update(self, validated_data):
        w = Workflow.objects.get(pk=self.context.get('workflow_id'))
        v, new_version = Version.objects.update_or_create(
            workflow=w,
            yw_model_checksum=validated_data.get('model_checksum'),
            defaults={
                'yw_model_output': validated_data.get('model'),
                'yw_graph_output': validated_data.get('graph'),
                'last_modified':datetime.datetime.now(tz=timezone.utc)
            }
        )
        v.save()
        r = Run(
            version=v,
            run_time_stamp=datetime.datetime.now(tz=timezone.utc),
            yw_recon_output=validated_data.get('recon')
        )
        r.save()

        tags = TagSerializer(validated_data.get('tags'), many=True)
        for tag in tags.data:
            t = Tag(parent_tag=None, tag_type=Workflow, title=tag.get('title'))
            t.save()

        scripts = ScriptSerializer(validated_data.get('scripts'), many=True)
        for script in scripts.data:
            s = Script(name=script.get('name'), version=v, checksum=script.get('checksum'), content=script.get('content'))
            s.save()

        files = FileSerializer(validated_data.get('files'), many=True)
        for file in files.data:
            f, _ = File.objects.update_or_create(
                checksum=file.get('checksum'),
                defaults={                
                    'size':file.get('size'),
                    'name':file.get('name'),
                    'uri':file.get('uri'),
                    'last_modified':file.get('last_modified')
                }
            )
            f.save()

        return w.pk, v.pk, r.pk, new_version
