from django.db import models

# Create your models here.

class Tag(models.Model):
    parent_tag = models.ForeignKey('self', blank=True, on_delete=models.DO_NOTHING, default=None)

    WORKFLOW = "w"
    VERSION = "v"
    RUN = "r"

    TAG_CHOICES = (
        (WORKFLOW, "Workflow"),
        (VERSION, "Version"),
        (RUN, "Run"),
    )

    title = models.CharField(max_length=255)
    tag_type = models.CharField(max_length=1, choices=TAG_CHOICES, default=WORKFLOW)

class WorkFlow(models.Model):
    # TODO: integrate users with yw database
    # user_id = models.ForeignKey() 
    workflow_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Version(models.Model):
    workflow_id = models.ForeignKey(WorkFlow, on_delete=models.CASCADE)
    version_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # TODO: double check checksum is same length as hash length client side
    script_check_sum = models.CharField(max_length=20)
    yw_model_check_sum = models.CharField(max_length=20)

    yw_model_output = models.CharField(max_length=255)
    yw_graph_output = models.TextField()

    last_modified = models.DateField()

class Run(models.Model):
    run_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    time_stamp = models.DateTimeField()
    yw_recon_output = models.TextField()

class File(models.Model):
    checksum = models.CharField(max_length=20, primary_key=True)
    file_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    input_data = models.FileField(upload_to="recon_files/", blank=True)

class RunFile(models.Model):
    run_id = models.ForeignKey(Run, on_delete=models.CASCADE)
    file_id = models.ForeignKey(File, on_delete=models.CASCADE)

    uri = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    time_stamp = models.DateField()
