from django.db import models

# Create your models here.

class Tag(models.Model):
    parent_tag = models.ForeignKey('self', blank=True, on_delete=models.DO_NOTHING, default=None)

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

class WorkFlow(models.Model):
    # TODO: integrate users with yw database
    # user_id = models.ForeignKey() 
    workflow_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField()

class Version(models.Model):
    workflow_id = models.ForeignKey(WorkFlow, on_delete=models.CASCADE)

    script_check_sum = models.CharField(max_length=128)
    yw_model_check_sum = models.CharField(max_length=128)

    yw_model_output = models.TextField()
    yw_graph_output = models.TextField()

    last_modified = models.DateTimeField()

class Run(models.Model):
    version_id = models.ForeignKey(Version, on_delete=models.CASCADE)

    run_time_stamp = models.DateTimeField()
    yw_recon_output = models.TextField()

class File(models.Model):
    file_checksum = models.CharField(max_length=128, primary_key=True)
    input_data = models.FileField(upload_to="recon_files/", blank=True)

class RunFile(models.Model):
    run_id = models.ForeignKey(Run, on_delete=models.CASCADE)
    file_id = models.ForeignKey(File, on_delete=models.CASCADE)

    uri = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    last_modified_time_stamp = models.DateTimeField()
    file_size = models.IntegerField()

class TagWorkflow(models.Model):
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    workflow_id = models.ForeignKey(WorkFlow, on_delete=models.CASCADE)

class TagVersion(models.Model):
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    version_id = models.ForeignKey(Version, on_delete=models.CASCADE)

class TagRun(models.Model):
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    run_id = models.ForeignKey(Run, on_delete=models.CASCADE)

class TagFile(models.Model):
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    file_id = models.ForeignKey(File, on_delete=models.CASCADE)
