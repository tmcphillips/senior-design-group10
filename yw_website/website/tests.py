import os
from django.test import TestCase
from django.test.client import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from website.views import model_form_upload


# class UploadTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()

#     def test_upload(self):
#         # Create dummy file to upload to Django
#         file_name = "file.txt"
#         f = SimpleUploadedFile(file_name, b"file_content")

#         # Send dummy request to upload view
#         post_test = self.client.post(path='/', data={'document': f})
#         model_form_upload(post_test.wsgi_request)

#         # Assert that file was successfully uploaded to our system
#         file_path = os.getcwd() + "/media/documents/" + file_name
#         self.assertTrue(os.path.isfile(file_path))

#         # Clean up after test
#         os.remove(file_path)
#         self.assertFalse(os.path.isfile(file_path))
