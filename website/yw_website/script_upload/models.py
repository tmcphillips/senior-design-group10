from django.db import models


class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)

class Document(models.Model):
	# username = models.ForeignKey(User, on_delete=models.CASCADE)
	# title = models.CharField(max_length=255, blank=True)
	# workflow = Image.open(model_instance.image_field)
	description = models.CharField(max_length=255, blank=True)
	document = models.FileField(upload_to='documents/')
	uploaded_at = models.DateTimeField(auto_now_add=True)

