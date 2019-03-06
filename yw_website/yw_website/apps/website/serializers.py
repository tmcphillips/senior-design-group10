from rest_framework import serializers

from .models import *
import datetime

from django.core.exceptions import ObjectDoesNotExist


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        exclude = ("version",)


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = "__all__"


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = "__all__"


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = "__all__"


class FileSerializer(serializers.ModelSerializer):
    lastModified = serializers.DateTimeField(source="last_modified")

    class Meta:
        model = File
        fields = ("checksum", "size", "name", "uri", "lastModified")


class RunFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunFile
        fields = "__all__"


class TagWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagWorkflow
        fields = "__all__"


class TagVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagVersion
        fields = "__all__"


class TagRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagRun
        fields = "__all__"


class TagFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagFile
        fields = "__all__"


class ProgramBlockSerializer(serializers.ModelSerializer):
    programBlockId = serializers.IntegerField(source="program_block_id")
    qualifiedName = serializers.CharField(source="qualified_name")
    inProgramBlock = serializers.IntegerField(
        source="in_program_block", required=False, allow_null=True
    )

    class Meta:
        model = ProgramBlock
        fields = ("programBlockId", "name", "qualifiedName", "inProgramBlock")


class DataSerializer(serializers.ModelSerializer):
    dataId = serializers.IntegerField(source="data_id")
    qualifiedName = serializers.CharField(source="qualified_name")
    inProgramBlock = serializers.IntegerField(
        source="in_program_block", required=False, allow_null=True
    )

    class Meta:
        model = Data
        fields = ("dataId", "name", "qualifiedName", "inProgramBlock")


class PortSerializer(serializers.ModelSerializer):
    portId = serializers.IntegerField(source="port_id")
    data = serializers.IntegerField()
    onProgramBlock = serializers.IntegerField(source="on_program_block", required=False)
    qualifiedName = serializers.CharField(source="qualified_name")
    alias = serializers.CharField(allow_null=True, allow_blank=True)
    uriTemplate = serializers.CharField(
        source="uri_template", allow_null=True, allow_blank=True
    )
    inPort = serializers.BooleanField(source="is_inport")
    outPort = serializers.BooleanField(source="is_outport")

    class Meta:
        model = Port
        fields = (
            "portId",
            "data",
            "name",
            "qualifiedName",
            "alias",
            "uriTemplate",
            "inPort",
            "outPort",
            "onProgramBlock",
        )


class ChannelSerializer(serializers.ModelSerializer):
    channelId = serializers.IntegerField(source="channel_id")
    outPort = serializers.IntegerField(source="out_port")
    inPort = serializers.IntegerField(source="in_port")
    data = serializers.IntegerField()
    isInflow = serializers.BooleanField(source="is_inflow")
    isOutflow = serializers.BooleanField(source="is_outflow")

    class Meta:
        model = Channel
        fields = ("channelId", "outPort", "inPort", "data", "isInflow", "isOutflow")


class UriVariableSerializer(serializers.ModelSerializer):
    uriVariableId = serializers.IntegerField(source="uri_variable_id")
    port = serializers.IntegerField()

    class Meta:
        model = UriVariable
        fields = ("uriVariableId", "port", "name")


class ResourceSerializer(serializers.ModelSerializer):
    resourceId = serializers.IntegerField(source="resource_id")
    data = serializers.IntegerField()

    class Meta:
        model = Resource
        fields = ("resourceId", "data", "uri")


class UriVariableValueSerializer(serializers.ModelSerializer):
    uriVariableId = serializers.IntegerField(source="uri_variable_id")
    resource = serializers.IntegerField()

    class Meta:
        model = UriVariableValue
        fields = ("uriVariableId", "resource", "value")


class YesWorkflowSaveSerializer(serializers.ModelSerializer):
    model = serializers.CharField(required=True, allow_blank=False)
    modelChecksum = serializers.CharField(
        required=True, allow_blank=True, max_length=128
    )
    graph = serializers.CharField(required=True, allow_blank=False)
    tags = serializers.ListField(
        child=serializers.CharField(required=False, allow_blank=True, max_length=32),
        default=None,
        allow_null=True,
    )
    title = serializers.CharField(
        required=False, default="", allow_blank=True, allow_null=False
    )
    description = serializers.CharField(
        required=False, default="", allow_blank=True, allow_null=False
    )
    scripts = ScriptSerializer(required=True, many=True)
    files = FileSerializer(many=True, default=None, allow_null=True)
    programBlock = ProgramBlockSerializer(many=True, default=None, allow_null=True)
    data = DataSerializer(many=True, default=None, allow_null=True)
    port = PortSerializer(many=True, default=None, allow_null=True)
    channel = ChannelSerializer(many=True, default=None, allow_null=True)
    uriVariable = UriVariableSerializer(many=True, default=None, allow_null=True)
    resource = ResourceSerializer(many=True, default=None, allow_null=True)
    uriVariableValue = UriVariableValueSerializer(
        many=True, default=None, allow_null=True
    )

    class Meta:
        model = Workflow
        fields = (
            "title",
            "description",
            "model",
            "modelChecksum",
            "graph",
            "tags",
            "scripts",
            "files",
            "programBlock",
            "data",
            "port",
            "channel",
            "uriVariable",
            "resource",
            "uriVariableValue",
        )

    def validate_scripts(self, attrs):
        if len(attrs) == 0:
            raise serializers.ValidationError("at least one script required")
        return attrs

    def create(self, validated_data):
        w = Workflow(
            user=self.context.get("username"),
            title=validated_data.get("title"),
            description=validated_data.get("description"),
        )
        w.save()
        v = Version(
            workflow=w,
            yw_model_checksum=validated_data.get("modelChecksum"),
            yw_model_output=validated_data.get("model"),
            yw_graph_output=validated_data.get("graph"),
            last_modified=datetime.datetime.now(tz=timezone.utc),
        )
        v.save()
        r = self._create_update_helper(w, v, validated_data)
        return w.pk, v.pk, r.pk

    def update(self, validated_data):
        w = Workflow.objects.get(pk=self.context.get("workflow_id"))
        v, new_version = Version.objects.update_or_create(
            workflow=w,
            yw_model_checksum=validated_data.get("modelChecksum"),
            defaults={
                "yw_model_output": validated_data.get("model"),
                "yw_graph_output": validated_data.get("graph"),
                "last_modified": datetime.datetime.now(tz=timezone.utc),
            },
        )
        v.save()
        r = self._create_update_helper(w, v, validated_data)

        return w.pk, v.pk, r.pk, new_version

    def _create_update_helper(self, w, v, validated_data):
        r = self._create_run(v, validated_data)
        self._create_tags(w, validated_data)
        self._create_scripts(v, validated_data)
        self._create_files(r, validated_data)
        self._create_program_blocks(r, validated_data)
        self._create_data(r, validated_data)
        self._create_ports(r, validated_data)
        self._create_channels(r, validated_data)
        self._create_uri_variables(r, validated_data)
        self._create_resources(r, validated_data)
        self._create_uri_variable_values(r, validated_data)
        return r

    def _create_run(self, v, validated_data):
        r = Run(version=v, run_time_stamp=datetime.datetime.now(tz=timezone.utc))
        r.save()
        return r

    def _create_tags(self, w, validated_data):
        tags = validated_data.get("tags")
        if tags:
            for tag in tags:
                if not TagWorkflow.objects.filter(tag__title=tag, workflow=w).exists():
                    t = Tag(parent_tag=None, tag_type=Workflow, title=tag)
                    t.save()
                    tw = TagWorkflow(tag=t, workflow=w)
                    tw.save()

    def _create_scripts(self, v, validated_data):
        scripts = ScriptSerializer(validated_data.get("scripts"), many=True)
        for script in scripts.data:
            s = Script(
                name=script.get("name"),
                version=v,
                checksum=script.get("checksum"),
                content=script.get("content"),
            )
            s.save()

    def _create_files(self, r, validated_data):
        files = FileSerializer(validated_data.get("files"), many=True)
        for file in files.data:
            f, _ = File.objects.update_or_create(
                checksum=file.get("checksum"),
                defaults={
                    "size": file.get("size"),
                    "name": file.get("name"),
                    "uri": file.get("uri"),
                    "last_modified": file.get("lastModified"),
                },
            )
            f.save()
            rf = RunFile(run=r, file=f)
            rf.save()

    def _create_program_blocks(self, r, validated_data):
        program_blocks = ProgramBlockSerializer(
            validated_data.get("programBlock"), many=True, context={"run": r}
        )
        for program_block in program_blocks.data:
            if program_block.get('inProgramBlock') != None:
                try:
                    in_block = ProgramBlock.objects.get(
                        programblock_id=program_block.get("inProgramBlock"), run=r
                    )
                except ObjectDoesNotExist:
                    raise serializers.ValidationError("Parent programblock does not exist when trying to create programBlock")
            else:
                in_block = None
            pb = ProgramBlock(
                programblock_id=program_block.get("programBlockId"),
                name=program_block.get("name"),
                qualified_name=program_block.get("qualifiedName"),
                in_program_block=in_block,
                run=r,
            )
            pb.save()

    def _create_data(self, r, validated_data):
        datas = DataSerializer(
            validated_data.get("data"), many=True, context={"run": r}
        )
        for data in datas.data:
            if data.get('inProgramBlock') != None:
                try:
                    in_block = ProgramBlock.objects.get(
                        programblock_id=data.get("inProgramBlock"), run=r
                    )
                except ObjectDoesNotExist:
                    raise serializers.ValidationError("inProgramBlock not found in Data")
            else:
                in_block = None

            d = Data(
                data_id=data.get("dataId"),
                name=data.get("name"),
                qualified_name=data.get("qualifiedName"),
                in_program_block=in_block,
                run=r,
            )
            d.save()

    def _create_ports(self, r, validated_data):
        ports = PortSerializer(
            validated_data.get("port"), many=True, context={"run": r}
        )
        for port in ports.data:
            try:
                in_block = ProgramBlock.objects.get(
                    programblock_id=port.get("onProgramBlock"), run=r
                )
                data = Data.objects.get(data_id=port.get("data"), run=r)
            except ObjectDoesNotExist:
                raise serializer.ValidationError(
                    "Could not get onProgramBlock when creating ports"
                )

            p = Port(
                port_id=port.get("portId"),
                on_program_block=in_block,
                data=data,
                name=port.get("name"),
                qualified_name=port.get("qualifiedName"),
                alias=port.get("alias"),
                uri_template=port.get("uriTemplate"),
                is_inport=port.get("inPort"),
                is_outport=port.get("outPort"),
                run=r,
            )
            p.save()

    def _create_channels(self, r, validated_data):
        channels = ChannelSerializer(validated_data.get("channel"), many=True)
        for channel in channels.data:
            try:
                out_port = Port.objects.get(port_id=channel.get("outPort"), run=r)
                in_port = Port.objects.get(port_id=channel.get("inPort"), run=r)
                data = Data.objects.get(data_id=channel.get("data"), run=r)
            except ObjectDoesNotExist:
                raise serializer.ValidationError(
                    "Could not create channels due to either outPort, inPort, or data being missing"
                )

            c = Channel(
                channel_id=channel.get("channelId"),
                out_port=out_port,
                in_port=in_port,
                data=data,
                is_inflow=channel.get("isInflow"),
                is_outflow=channel.get("isOutflow"),
                run=r,
            )
            c.save()

    def _create_uri_variables(self, r, validated_data):
        uris = UriVariableSerializer(validated_data.get("uriVariable"), many=True)
        for uri in uris.data:
            try:
                port = Port.objects.get(port_id=uri.get("port"), run=r)
            except ObjectDoesNotExist:
                raise serializer.ValidationError(
                    "Could not get port when creating uri variable"
                )

            u = UriVariable(
                uri_variable_id=uri.get("uriVariableId"),
                port=port,
                name=uri.get("name"),
                run=r,
            )
            u.save()

    def _create_resources(self, r, validated_data):
        resources = ResourceSerializer(validated_data.get("resource"), many=True)
        for resource in resources.data:
            try:
                data = Data.objects.get(data_id=resource.get("data"), run=r)
            except ObjectDoesNotExist:
                raise serializer.ValidationError(
                    "Could not get data when creating resources"
                )

            r = Resource(
                resource_id=resource.get("resourceId"),
                data=data,
                uri=resource.get("uri"),
                run=r,
            )
            r.save()

    def _create_uri_variable_values(self, r, validated_data):
        uri_values = UriVariableValueSerializer(
            validated_data.get("uriVariableValue"), many=True
        )
        for uri_value in uri_values.data:
            try:
                uri_variable = UriVariable.objects.get(
                    uri_variable_id=uri_value.get("uriVariableId"), run=r
                )
                resource = Resource.objects.get(
                    resource_id=uri_value.get("resource"), run=r
                )
            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    "Could not get the proper uri variable and resource values when creating uri variable values"
                )

            uv = UriVariableValue(
                uri_variable=uri_variable,
                resource=resource,
                value=uri_value.get("value"),
                run=r,
            )
            uv.save()
