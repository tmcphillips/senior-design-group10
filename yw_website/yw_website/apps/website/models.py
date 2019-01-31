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

    title = models.CharField(max_length=255)
    tag_type = models.CharField(
        max_length=1, choices=TAG_CHOICES, default=WORKFLOW)


class Workflow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=255)
    description = models.TextField()


class Version(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, null=True)

    script_check_sum = models.CharField(max_length=128)
    yw_model_check_sum = models.CharField(max_length=128)

    yw_model_output = models.TextField()
    yw_graph_output = models.TextField()

    last_modified = models.DateTimeField()


class Run(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE, null=True)

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
    run = models.ForeignKey(Run, on_delete=models.CASCADE, null=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, null=True)

    uri = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)


class TagWorkflow(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('tag', 'workflow')


class TagVersion(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    version = models.ForeignKey(Version, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('tag', 'version')


class TagRun(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    run = models.ForeignKey(Run, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('tag', 'run')


class TagFile(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('tag', 'file')
