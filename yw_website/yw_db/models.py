from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Tag(models.Model):
    parent_tag_id = models.ForeignKey('self', related_name='parent_tag', on_delete=models.DO_NOTHING, null=True)

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
    tag_type = models.CharField(max_length=1, choices=TAG_CHOICES, default=WORKFLOW)

class Workflow(models.Model):
    user_id = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE, null=True) 

    title = models.CharField(max_length=255)
    description = models.TextField()

class Version(models.Model):
    workflow_id = models.ForeignKey(Workflow, related_name="workflows", on_delete=models.CASCADE, null=True)

    script_check_sum = models.CharField(max_length=128)
    yw_model_check_sum = models.CharField(max_length=128)

    yw_model_output = models.TextField()
    yw_graph_output = models.TextField()

    last_modified = models.DateTimeField()

class Run(models.Model):
    version_id = models.ForeignKey(Version, related_name='versions', on_delete=models.CASCADE, null=True)

    run_time_stamp = models.DateTimeField()
    yw_recon_output = models.TextField()

class File(models.Model):
    file_checksum = models.CharField(max_length=128, primary_key=True, default=None)
    input_data = models.FileField(upload_to="recon_files/")
    file_size = models.IntegerField(default=0)

    last_modified_time_stamp = models.DateTimeField(default=timezone.now())

class RunFile(models.Model):
    run_id = models.ForeignKey(Run, related_name='run_file', on_delete=models.CASCADE, null=True)
    file_id = models.ForeignKey(File, related_name='file_run', on_delete=models.CASCADE, null=True)

    uri = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)

class TagWorkflow(models.Model):
    tag_id = models.ForeignKey(Tag, related_name='tags_workflows', on_delete=models.CASCADE, null=True)
    workflow_id = models.ForeignKey(Workflow, related_name='workflows_tags', on_delete=models.CASCADE, null=True)

class TagVersion(models.Model):
    tag_id = models.ForeignKey(Tag, related_name='tags_versions', on_delete=models.CASCADE, null=True)
    version_id = models.ForeignKey(Version, related_name='versions_tags', on_delete=models.CASCADE, null=True)

class TagRun(models.Model):
    tag_id = models.ForeignKey(Tag, related_name='tags_runs', on_delete=models.CASCADE, null=True)
    run_id = models.ForeignKey(Run, related_name='runs_tags', on_delete=models.CASCADE, null=True)

class TagFile(models.Model):
    tag_id = models.ForeignKey(Tag, related_name='tags_files', on_delete=models.CASCADE, null=True)
    file_id = models.ForeignKey(File, related_name='files_tags', on_delete=models.CASCADE, null=True)
