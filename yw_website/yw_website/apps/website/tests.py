import uuid

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from rest_framework.test import APIClient
import json
import datetime
from .models import Workflow
from .serializers import *

class DBTestCase(TestCase):
    def setUp(self):
        self.w = Workflow.objects.create()
        self.w.save()

    def test_workflow_save(self):
        c = Client()

        route = "/api/v1/workflows/{}/".format(self.w.id)
        response = c.get(route)

        self.assertEquals(response.status_code, 200,
                          "Database did not properly populate api")

    def tearDown(self):
        Workflow.delete(self.w)


class YwSaveTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = str(uuid.uuid1())
        self.user = User.objects.create_user(
            username=self.username, password='12345')

    def test_yw_ping(self):
        route = '/save/ping/'
        response = self.client.get(path=route)
        self.assertEqual(response.status_code, 200, msg="Valid route failed")

    def test_bad_yw_ping(self):
        bad_route = '/save/pig/'
        bad_response = self.client.get(path=bad_route)
        self.assertNotEqual(bad_response.status_code, 200,
                            msg="Invalid route failed")

    def test_save_upload(self):
        route = '/save/'
        now = datetime.datetime.now()
        data = {}
        data["username"] = self.username
        data["title"] = "test_title"
        data["description"] = "test_description"
        data["model"] = "test_model"
        data["model_checksum"] = str(uuid.uuid1())
        data["graph"] = "test_graph"
        data["recon"] = "test_recon"
        data["tags"] = ["tag_1", "tag_2", "tag_3"]
        data["scripts"] = [{"name":"script_1", "checksum":str(uuid.uuid1()), "content":"script_1_content"},
                            {"name":"script_2", "checksum":str(uuid.uuid1()), "content":"script_2_content"},
                            {"name":"script_3", "checksum":str(uuid.uuid1()), "content":"script_3_content"}]
        data["files"] = [{"name":"file_name_1", "checksum":str(uuid.uuid1()), "size":3, "uri":"file_uri1", "last_modified":now},
                        {"name":"file_name_2", "checksum":str(uuid.uuid1()), "size":9, "uri":"file_uri2", "last_modified":now}]

        response = self.client.post(route, data, format='json')
        
        self.assertEquals(response.status_code, 200,
                          msg="Could not upload a workflow")

        data['username'] = 'nousername'
        bad_response = self.client.post(route, data, format='json')
        self.assertNotEqual(bad_response.status_code, 200,
                            msg="Bad username unaccounted by save path")
        data['username'] = self.username
        data['tags'] = 'bad_tag_data'
        bad_response = self.client.post(route, data, format='json')
        self.assertNotEqual(bad_response.status_code, 200,
                            msg="Bad tag json format")

    def test_workflow_update(self):
        route = '/save/'
        data = {}
        now = datetime.datetime.now()
        data["username"] = self.username
        data["title"] = "test_title"
        data["description"] = "test_description"
        data["model"] = "test_model"
        data["model_checksum"] = str(uuid.uuid1())
        data["graph"] = "test_graph"
        data["recon"] = "test_recon"
        data["tags"] = ["tag_1", "tag_2", "tag_3"]
        data["scripts"] = [{"name":"script_1", "checksum":str(uuid.uuid1()), "content":"script_1_content"},
                            {"name":"script_2", "checksum":str(uuid.uuid1()), "content":"script_2_content"},
                            {"name":"script_3", "checksum":str(uuid.uuid1()), "content":"script_3_content"}]
        data["files"] = [{"name":"file_name_1", "checksum":str(uuid.uuid1()), "size":3, "uri":"file_uri1", "last_modified":now},
                        {"name":"file_name_2", "checksum":str(uuid.uuid1()), "size":9, "uri":"file_uri2", "last_modified":now}]


        response = self.client.post(route, data, format='json')
        first_workflow_id = response.data['workflowId']
        first_version_num = response.data['versionNumber']

        data['model_checksum'] = str(uuid.uuid1())
        data["files"] = [{"name":"file_name_3", "checksum":str(uuid.uuid1()), "size":3, "uri":"file_uri1", "last_modified":now},
                        {"name":"file_name_4", "checksum":str(uuid.uuid1()), "size":9, "uri":"file_uri2", "last_modified":now}]

        route = '/save/{}/'.format(first_workflow_id)

        response = self.client.post(route, data, format='json')
        second_workflow_id = response.data['workflowId']
        second_version_num = response.data['versionNumber']

        self.assertEqual(first_workflow_id, second_workflow_id,
                         msg="A new workflow was created for the same workflow.")
        self.assertNotEqual(first_version_num, second_version_num,
                            msg="Version was not incremented when a new model checksum was uploaded")

    def test_bad_workflow_update(self):
        data = {}
        data['workflow_id'] = -1
        data['username'] = self.username
        data['title'] = 'test_title'
        data['description'] = 'test_description'
        data['model'] = 'test_model'
        data['model_checksum'] = str(uuid.uuid1())
        data['graph'] = 'test_graph'
        data['recon'] = 'test_recon'

        route = '/save/{}/'.format(data['workflow_id'])

        response = self.client.post(route, data)
        self.assertEqual(response.status_code, 404,
                         msg="Workflow does not exist")
