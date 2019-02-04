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

    yw_model_check_sum = models.CharField(max_length=128)

    yw_model_output = models.TextField()
    yw_graph_output = models.TextField()

    last_modified = models.DateTimeField()


class Script(models.Model):
    script_check_sum = models.CharField(max_length=128)
    script = models.FileField(
        upload_to='workflow_scripts/', null=True, default=None)


class VersionScript(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE, blank=False)
    script = models.ForeignKey(Script, on_delete=models.CASCADE, blank=False)


class Run(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE, blank=False)

    run_time_stamp = models.DateTimeField()
    yw_recon_output = models.TextField()


class File(models.Model):
    file_checksum = models.CharField(
        max_length=128, primary_key=True, default=None)
    input_data = models.FileField(
        upload_to="recon_files/", null=True, default=None)
    file_size = models.IntegerField(default=0)

    last_modified = models.DateTimeField(default=timezone.now())


class RunFile(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE, blank=False)
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=False)

    uri = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)


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
