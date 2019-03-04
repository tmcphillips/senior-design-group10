from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    parent_tag = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, null=True)

    FILE = "f"
    WORKFLOW = "w"
    VERSION = "v"
    RUN = "r"

    TAG_CHOICES = (
        (WORKFLOW, "Workflow"),
        (VERSION, "Version"),
        (RUN, "Run"),
        (FILE, "File"),
    )

    title = models.CharField(max_length=32)
    tag_type = models.CharField(
        max_length=1, choices=TAG_CHOICES, default=WORKFLOW)


class Workflow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=255)
    description = models.TextField()


class Version(models.Model):
    workflow = models.ForeignKey(
        Workflow, on_delete=models.CASCADE, blank=False)

    yw_model_checksum = models.CharField(max_length=128)

    yw_model_output = models.TextField()
    yw_graph_output = models.TextField()

    last_modified = models.DateTimeField()


class Script(models.Model):
    name = models.TextField()
    version = models.ForeignKey(Version, on_delete=models.CASCADE, blank=False)
    checksum = models.CharField(max_length=128)
    content = models.TextField()

class Run(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE, blank=False)

    run_time_stamp = models.DateTimeField()
    yw_recon_output = models.TextField()


class File(models.Model):
    checksum = models.CharField(
        max_length=128)
    size = models.IntegerField(default=0)
    name = models.TextField()
    uri = models.TextField()

    last_modified = models.DateTimeField()


class RunFile(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE, blank=False)
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=False)


class TagWorkflow(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=False)
    workflow = models.ForeignKey(
        Workflow, on_delete=models.CASCADE, blank=False)

    class Meta:
        unique_together = ('tag', 'workflow')


class TagVersion(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=False)
    version = models.ForeignKey(Version, on_delete=models.CASCADE, blank=False)

    class Meta:
        unique_together = ('tag', 'version')


class TagRun(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=False)
    run = models.ForeignKey(Run, on_delete=models.CASCADE, blank=False)

    class Meta:
        unique_together = ('tag', 'run')


class TagFile(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=False)
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=False)

    class Meta:
        unique_together = ('tag', 'file')

class ProgramBlock(models.Model):
    class Meta:
        unique_together = ('programblock_id', 'run')
    programblock_id = models.IntegerField()
    name = models.TextField()
    qualified_name = models.TextField()
    in_program_block = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, null=True)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)

class Data(models.Model):
    class Meta:
        unique_together = ('data_id', 'run')
    data_id = models.IntegerField()
    name = models.TextField()
    in_program_block = models.ForeignKey(ProgramBlock, on_delete=models.DO_NOTHING, null=True)
    name = models.TextField()
    qualifiedName = models.TextField()
    run = models.ForeignKey(Version, on_delete=models.CASCADE)

class Port(models.Model):
    class Meta:
        unique_together = ('port_id', 'run')
    port_id = models.IntegerField()
    on_program_block = models.ForeignKey(ProgramBlock, on_delete=models.DO_NOTHING)
    data = models.ForeignKey(Data, on_delete=models.DO_NOTHING)
    name = models.TextField()
    qualifed_name = models.TextField()
    alias = models.TextField(null=True)
    uri_template = models.TextField(null=True)
    is_inport = models.BooleanField()
    is_outport = models.BooleanField()
    run = models.ForeignKey(Run, on_delete=models.CASCADE)

class Channel(models.Model):
    class Meta:
        unique_together = ('channel_id', 'run')
    channel_id = models.IntegerField()
    out_port = models.ForeignKey(Port, on_delete=models.DO_NOTHING, related_name="inport")
    in_port = models.ForeignKey(Port, on_delete=models.DO_NOTHING, related_name="outport")
    data = models.ForeignKey(Data, on_delete=models.DO_NOTHING)
    is_inflow = models.BooleanField()
    is_outflow = models.BooleanField()
    run = models.ForeignKey(Run, on_delete=models.CASCADE)

class UriVariable(models.Model):
    class Meta:
        unique_together = ('uri_variable_id', 'run')
    uri_variable_id = models.IntegerField()
    port = models.ForeignKey(Port, on_delete=models.DO_NOTHING)
    name = models.TextField()
    run = models.ForeignKey(Run, on_delete=models.CASCADE)

class Resource(models.Model):
    class Meta:
        unique_together = ('resource_id', 'run')
    resource_id = models.IntegerField()
    data = models.ForeignKey(Data, on_delete=models.DO_NOTHING)
    uri = models.TextField()
    run = models.ForeignKey(Run, on_delete=models.CASCADE)

class UriVariableValue(models.Model):
    class Meta:
        unique_together = ('uri_variable_value_id', 'run')
    uri_variable_value_id = models.IntegerField()
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    uri_variable = models.ForeignKey(UriVariable, on_delete=models.DO_NOTHING)
    resource = models.ForeignKey(Resource, on_delete=models.DO_NOTHING)
    value = models.TextField()
