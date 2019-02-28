from rest_framework import serializers

from .models import *
import datetime 


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

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
    lastModified = serializers.DateTimeField(source='last_modified')
    
    class Meta:
        model = File
        fields = (
            'checksum',
            'size',
            'name',
            'uri',
            'lastModified',
        )


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
        
class ProgramBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramBlock
        fields = ('program_block_id', 'name', 'qualified_name', 'in_program_block') 

class YesWorkflowSaveSerializer(serializers.ModelSerializer):
    model = serializers.CharField(required=True, allow_blank=False)
    modelChecksum = serializers.CharField(required=True, allow_blank=True, max_length=128)
    graph = serializers.CharField(required=True, allow_blank=False)
    tags = serializers.ListField(
        child=serializers.CharField(required=False, allow_blank=True, max_length=32), default=None, allow_null=True
    )
    title = serializers.CharField(required=False, default='', allow_blank=True, allow_null=False)
    description = serializers.CharField(required=False, default='', allow_blank=True, allow_null=False)
    scripts = ScriptSerializer(required=True, many=True)
    files = FileSerializer(many=True, default=None, allow_null=True)
    programBlock = ProgramBlockSerializer(many=True, default=None, allow_null=True)

    class Meta:
        model = Workflow
        fields = ('title','description','model','modelChecksum', 'graph', 'tags', 'scripts', 'files', 'programBlock')
   
    def validate_scripts(self, attrs):
        if len(attrs) == 0:
            raise serializers.ValidationError('at least one script required')
        return attrs

    def create(self, validated_data):
        w = Workflow(
            user=self.context.get('username'),
            title=validated_data.get('title'),
            description=validated_data.get('description')
        )
        w.save()
        v = Version(
            workflow=w,
            yw_model_checksum=validated_data.get('modelChecksum'),
            yw_model_output=validated_data.get('model'),
            yw_graph_output=validated_data.get('graph'),
            last_modified=datetime.datetime.now(tz=timezone.utc)
        )
        v.save()
        r = self.__create_update_helper(w, v, validated_data)
        return w.pk, v.pk, r.pk
    
    def update(self, validated_data):
        w = Workflow.objects.get(pk=self.context.get('workflow_id'))
        v, new_version = Version.objects.update_or_create(
            workflow=w,
            yw_model_checksum=validated_data.get('modelChecksum'),
            defaults={
                'yw_model_output': validated_data.get('model'),
                'yw_graph_output': validated_data.get('graph'),
                'last_modified':datetime.datetime.now(tz=timezone.utc)
            }
        )
        v.save()
        r = self.__create_update_helper(w, v, validated_data)
        return w.pk, v.pk, r.pk, new_version

    def __create_update_helper(self, w, v, validated_data):
        r = Run(
            version=v,
            run_time_stamp=datetime.datetime.now(tz=timezone.utc),
        )
        r.save()

        # TODO: Check if tags already exist
        tags = validated_data.get('tags')
        if tags:
            for tag in tags:
                t = Tag(parent_tag=None, tag_type=Workflow, title=tag)
                t.save()
                tw = TagWorkflow(tag=t, workflow=w)
                tw.save()

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
                    'last_modified':file.get('lastModified')
                }
            )
            f.save()
            rf = RunFile(run=r, file=f)
            rf.save()

        program_blocks = ProgramBlockSerializer(validated_data.get('programBlock'), many=True)
        for program_block in program_blocks.data:
            # NOTE: Assumes that parent program block already exists
            try: 
                in_block = ProgramBlock.objects.get(program_block_id=validated_data.get('inProgramBlock'), version=v)
            except ProgramBlock.DoesNotExist:
                in_block = None

            pb = ProgramBlock(program_block_id=program_block.get('program_block_id'), in_program_block=in_block, version=v) 
            pb.save()
            print(program_block)
        return r
