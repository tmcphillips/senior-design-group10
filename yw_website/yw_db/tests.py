from django.test import TestCase
from django.test.client import Client
from yw_db.models import Workflow

class DBTestCase(TestCase):
    def setUp(self):
        self.w = Workflow.objects.create()
        self.w.save()
        
    def test_workflow_save(self):
        c = Client()

        route = "/api/v1/workflows/{}/".format(self.w.id)
        response = c.get(route)

        self.assertEquals(response.status_code, 200, "Database did not properly populate api")

    def tearDown(self):
        Workflow.delete(self.w)
