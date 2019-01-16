from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from yw_db.models import Workflow
import uuid

class YwSaveTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = str(uuid.uuid1())
        self.user = User.objects.create_user(username=self.username, password='12345')

    def test_yw_ping(self):
        route = '/save/ping/'
        response = self.client.get(path=route)
        self.assertEqual(response.status_code, 200, msg="Valid route failed")

    def test_bad_yw_ping(self):
        bad_route = '/save/pig/'
        bad_response = self.client.get(path=bad_route)
        self.assertNotEqual(bad_response.status_code, 200, msg="Invalid route failed")

    def test_save_upload(self):
        route = '/save/'
        data = {}
        data['username'] = self.username
        data['title'] = 'test_title'
        data['description'] = 'test_description'
        data['model'] = 'test_model'
        data['model_checksum'] = '2341234123423'
        data['graph'] = 'test_graph'
        data['recon'] = 'test_recon'

        response = self.client.post(route, data)

        self.assertEquals(response.status_code, 200, msg="Could not upload a workflow")
        data['username'] = 'nousername'
        bad_response = self.client.post(route, data)
        self.assertNotEqual(bad_response.status_code, 200, msg="Bad username unaccounted by save path")

    def test_workflow_update(self):
        # After a workflow has a new checksum for it's model, a new version is created for that workflow
        route = '/save/'
        data = {}
        data['username'] = self.username
        data['title'] = 'test_title'
        data['description'] = 'test_description'
        data['model'] = 'test_model'
        data['model_checksum'] = 'a'
        data['graph'] = 'test_graph'
        data['recon'] = 'test_recon'

        response = self.client.post(route, data)
        first_workflow_id = response.data['workflow']['id']
        first_version_id = response.data['version']['id']

        data['model_checksum'] = 'b'
        data['workflow_id'] = first_workflow_id
        route = '/save/update/'

        response = self.client.post(route, data)
        second_workflow_id = response.data['workflow']['id']
        second_version_id = response.data['version']['id']

        self.assertEqual(first_workflow_id, second_workflow_id, msg="A new workflow was created for the same workflow.")
        self.assertNotEqual(first_version_id, second_version_id, msg="Version was not incremented when a new model checksum was uploaded")

    def test_bad_workflow_update(self):
        route = '/save/update/'
        data = {}
        data['workflow_id'] = -1
        data['username'] = self.username
        data['title'] = 'test_title'
        data['description'] = 'test_description'
        data['model'] = 'test_model'
        data['model_checksum'] = 'a'
        data['graph'] = 'test_graph'
        data['recon'] = 'test_recon'

        response = self.client.post(route, data)
        self.assertEqual(response.status_code, 500, msg="Unvalid Workflow id passed in post request")




