from rest_framework import serializers

from .models import *
import datetime
import time
import pytz
# from django.utils import timezone
from tzlocal import get_localzone
from dateutil import tz
import os

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
    onProgramBlock = serializers.IntegerField(source="on_program_block")
    qualifiedName = serializers.CharField(source="qualified_name")
    alias = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    uriTemplate = serializers.CharField(
        source="uri_template", allow_null=True, allow_blank=True, required=False
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
    lastModified = serializers.DateTimeField(source="last_modified")
    data = serializers.IntegerField()

    class Meta:
        model = Resource
        fields = ("resourceId", "data", "uri", "checksum", "name", "size", "lastModified")


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
            last_modified=self._utc_to_local(datetime.datetime.utcnow()),
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
                "last_modified": self._utc_to_local(datetime.datetime.utcnow()),
            },
        )
        v.save()
        r = self._create_update_helper(w, v, validated_data)

        return w.pk, v.pk, r.pk, new_version

    def _create_update_helper(self, w, v, validated_data):
        r = self._create_run(v, validated_data)
        self._create_tags(w, validated_data)
        self._create_scripts(v, validated_data)
        self._create_program_blocks(r, validated_data)
        self._create_data(r, validated_data)
        self._create_ports(r, validated_data)
        self._create_channels(r, validated_data)
        self._create_uri_variables(r, validated_data)
        self._create_resources(r, validated_data)
        self._create_uri_variable_values(r, validated_data)
        return r

    def _create_run(self, v, validated_data):
        r = Run(version=v, run_time_stamp=self._utc_to_local(datetime.datetime.utcnow()))
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
        channels = ChannelSerializer(validated_data.get("channel"), many=True, context={"run": r})
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
        uris = UriVariableSerializer(validated_data.get("uriVariable"), many=True, context={"run": r})
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
        resources = ResourceSerializer(validated_data.get("resource"), many=True, context={"run": r})
        for resource in resources.data:
            try:
                data = Data.objects.get(data_id=resource.get("data"), run=r)
            except ObjectDoesNotExist:
                raise serializer.ValidationError(
                    "Could not get data when creating resources"
                )

            new_resource = Resource(
                resource_id=resource.get("resourceId"),
                run=r,
                data=data,
                uri=resource.get("uri"),
                name=resource.get("name"),
                checksum=resource.get("checksum"),
                size=resource.get("size"),
                last_modified= self._utc_to_local(resource.get("lastModified")),
            )
            new_resource.save()

    def _create_uri_variable_values(self, r, validated_data):
        uri_values = UriVariableValueSerializer(
            validated_data.get("uriVariableValue"), many=True, context={"run": r}
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

    def _utc_to_local(self, utc):
        # local_tz = get_localzone()
        # print("THIS IS A TEST")
        # print(type(utc))
        # utc = utc.timestamp()
        # local_dt = utc.replace(tzinfo=pytz.utc).astimezone(local_tz)
        # new_utc = datetime.utcfromtimestamp(utc)
        # local_dt = new_utc.replace(tzinfo=pytz.utc).astimezone(local_tz)
        # local_dt = local_tz.fromutc(datetime.fromtimestamp(utc).replace(tzinfo=None))

        # local_tz = tz.tzlocal()
        # # return local_tz.normalize(local_dt)
        # now_timestamp = time.time()
        # offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
        # print("THIS IS A TEST")
        # print(utc)
        # new = utc + offset
        # new = new.astimezone(local_tz)
        # print("conversion")
        # print(new)
        # return new
        
        # print("testing")
        # print(utc)
        # print(type(utc))
        # now = datetime.datetime.utcnow()
        # local_dt = get_localzone()
        # utc_tz = tz.gettz('UTC')

        # # convert
        # print("replacing")
        # new = now.replace(tzinfo=utc_tz)
        # print(new)
        # print("converting")
        # print(new.astimezone(local_dt))

        # print("this is the timezone")
        # print(local_dt)
        
        # # print(new)
        # # print(type(new))
        # return new
        # my_tz_name = '/'.join(os.path.realpath('/etc/localtime').split('/')[-2:])


        my_tz_name = get_localzone()
        print('checking')
        print(my_tz_name)
        print(type(my_tz_name))
        # my_tz_name = datetime.datetime.now(tz.tzlocal())
        print('my Timezone: ', my_tz_name)
        my_tz = pytz.timezone(my_tz_name)
        print('testing: ', utc)
        utc = utc.replace(tzinfo=my_tz)
        print('converting', utc)
        # print(utc)
        return utc

