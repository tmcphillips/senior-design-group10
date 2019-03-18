import uuid

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
import json
import datetime
from .models import Workflow, TagWorkflow
from .serializers import *
import copy


class DBTestCase(TestCase):
    def setUp(self):
        self.w = Workflow.objects.create()
        self.w.save()

    def test_workflow_save(self):
        c = APIClient()

        route = "/api/v1/workflows/{}/".format(self.w.id)
        response = c.get(route)

        self.assertEquals(
            response.status_code, 200, "Database did not properly populate api"
        )

    def tearDown(self):
        Workflow.delete(self.w)


class YwSaveTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = str(uuid.uuid1())
        self.password = "Password!@#"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        
        res = self.client.post('/rest-auth/login/', data={'username': self.username, 'password': self.password}, format='json')
        self.token = res.data['key']
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.data = {}
        self.data["username"] = self.username
        self.data["title"] = "test_title"
        self.data["description"] = "test_description"
        self.data["model"] = "test_model"
        self.data["modelChecksum"] = str(uuid.uuid1())
        self.data["graph"] = "test_graph"
        self.data["recon"] = "test_recon"
        self.data["tags"] = ["tag_1", "tag_2", "tag_3"]
        self.data["scripts"] = [
            {
                "name": "script_1",
                "checksum": str(uuid.uuid1()),
                "content": "script_1_content",
            },
            {
                "name": "script_2",
                "checksum": str(uuid.uuid1()),
                "content": "script_2_content",
            },
            {
                "name": "script_3",
                "checksum": str(uuid.uuid1()),
                "content": "script_3_content",
            },
        ]
        self.data["files"] = [
            {
                "name": "file_name_1",
                "checksum": str(uuid.uuid1()),
                "size": 3,
                "uri": "file_uri1",
                "lastModified": datetime.datetime.now(),
            },
            {
                "name": "file_name_2",
                "checksum": str(uuid.uuid1()),
                "size": 9,
                "uri": "file_uri2",
                "lastModified": datetime.datetime.now(),
            },
        ]
        self.data["programBlock"] = [
            {
                "programBlockId": 1,
                "inProgramBlock": None,
                "name": "programBlock1",
                "qualifiedName": "programBlockQualifiedName",
            },
            {
                "programBlockId": 2,
                "inProgramBlock": 1,
                "name": "programBlock2",
                "qualifiedName": "programBlockQualifiedName2",
            },
        ]
        self.data["data"] = [
            {
                "dataId": 1,
                "inProgramBlock": 1,
                "name": "data1",
                "qualifiedName": "dataQualifiedName",
            },
            {
                "dataId": 2,
                "inProgramBlock": 1,
                "name": "dataName2",
                "qualifiedName": "dataQualifiedName2",
            },
        ]
        self.data["port"] = [
            {
                "portId": 1,
                "onProgramBlock": 1,
                "data": 1,
                "name": "PortOne",
                "qualifiedName": "portOneQualifiedName",
                "alias": None,
                "uriTemplate": None,
                "inPort": True,
                "outPort": False,
            },
            {
                "portId": 2,
                "onProgramBlock": 2,
                "data": 2,
                "name": "PortTwo",
                "qualifiedName": "portTwoQualifiedName",
                "alias": "aliasTwo",
                "uriTemplate": "uriTwo",
                "inPort": False,
                "outPort": True,
            },
        ]
        self.data["channel"] = [
            {
                "channelId": 1,
                "inPort": 1,
                "outPort": 2,
                "data": 1,
                "isInflow": True,
                "isOutflow": False,
            }
        ]
        self.data["uriVariable"] = [
            {"uriVariableId": 1, "port": 1, "name": "urivarname"}
        ]
        self.data["resource"] = [{"resourceId": 1, "data": 1, "uri": "urivar"}]
        self.data["uriVariableValue"] = [
            {"uriVariableId": 1, "resource": 1, "value": "uripath"}
        ]

    def test_yw_ping(self):
        route = "/save/ping/"
        response = self.client.get(path=route)
        self.assertEqual(response.status_code, 200, msg="Valid route failed")

    def test_bad_yw_ping(self):
        bad_route = "/save/pig/"
        bad_response = self.client.get(path=bad_route)
        self.assertNotEqual(bad_response.status_code, 200, msg="Invalid route failed")

    def test_save_upload(self):
        route = "/save/"
        response = self.client.post(route, self.data, format="json")

        self.assertEquals(
            response.status_code,
            200,
            msg="Could not upload a workflow: {}".format(response.data.get("error")),
        )

    def test_bad_save_upload(self):
        route = "/save/"
        data = copy.deepcopy(self.data)
        bad_client = copy.deepcopy(self.client)
        bad_client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token+'!@#$%^'))
        bad_response = bad_client.post(route, data, format="json")
        self.assertNotEqual(
            bad_response.status_code, 200, msg="Bad username unaccounted by save path"
        )
        data["username"] = self.username
        data["tags"] = "bad_tag_data"
        bad_response = self.client.post(route, data, format="json")
        self.assertNotEqual(bad_response.status_code, 200, msg="Bad tag json format")
        data["scripts"] = []
        bad_response = self.client.post(route, data, format="json")
        self.assertNotEqual(
            bad_response.status_code, 200, msg="One script needed for valid request"
        )

    def test_workflow_update(self):
        route = "/save/"
        data = copy.deepcopy(self.data)
        response = self.client.post(route, data, format="json")

        first_workflow_id = response.data["workflowId"]
        first_version_num = response.data["versionNumber"]

        data["modelChecksum"] = str(uuid.uuid1())
        data["files"] = [
            {
                "name": "file_name_3",
                "checksum": str(uuid.uuid1()),
                "size": 3,
                "uri": "file_uri1",
                "lastModified": datetime.datetime.now(),
            },
            {
                "name": "file_name_4",
                "checksum": str(uuid.uuid1()),
                "size": 9,
                "uri": "file_uri2",
                "lastModified": datetime.datetime.now(),
            },
        ]

        route = "/save/{}/".format(first_workflow_id)

        response = self.client.post(route, data, format="json")
        self.assertEqual(
            200,
            response.status_code,
            msg="Returned {}: {}".format(response.status_code, response.data),
        )

        second_workflow_id = response.data["workflowId"]
        second_version_num = response.data["versionNumber"]

        self.assertEqual(
            first_workflow_id,
            second_workflow_id,
            msg="A new workflow was created for the same workflow.",
        )
        self.assertNotEqual(
            first_version_num,
            second_version_num,
            msg="Version was not incremented when a new model checksum was uploaded",
        )
        self.assertTrue(
            response.data["newVersion"],
            msg="Server did not communicate a version change.",
        )

    def test_bad_workflow_update(self):
        data = copy.deepcopy(self.data)
        data["workflow_id"] = -1
        route = "/save/{}/".format(data["workflow_id"])

        response = self.client.post(route, data, format="json")
        self.assertEqual(response.status_code, 404, msg="Workflow does not exist")

    def test_bad_parent_program_block(self):
        data = copy.deepcopy(self.data)
        data["programBlock"] = [
            {
                "programBlockId": 2,
                "inProgramBlock": 1,
                "name": "programBlock1",
                "qualifiedName": "programBlockQualifiedName",
            },
            {
                "programBlockId": 1,
                "inProgramBlock": None,
                "name": "programBlock1",
                "qualifiedName": "programBlockQualifiedName",
            },
        ]
        route = "/save/"
        response = self.client.post(route, data, format="json")
        self.assertEqual(
            response.status_code,
            500,
            msg="Error creating validating parent ProgramBlocks",
        )

    def test_no_repeating_tags(self):
        data = copy.deepcopy(self.data)
        data["tags"].append("tag_1")
        route = "/save/"

        response = self.client.post(route, data, format="json")

        route = "/save/{}/".format(response.data["workflowId"])
        response = self.client.post(route, data, format="json")
        w = Workflow.objects.get(pk=response.data["workflowId"])
        wt = TagWorkflow.objects.filter(workflow=w)
        self.assertEqual(
            len(wt),
            len(data["tags"]) - 1,
            msg="Expected only three tags to be associated with workflow",
        )
