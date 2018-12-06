from django.test import TestCase
from django.test.client import Client
from yw_db.models import Workflow

# Create your tests here.

class DBTestCase(TestCase):
    def test_workflow_save(self):
        test = Workflow.objects.create(pk=1)
        c = Client()

        route = "/api/v1/workflows/1/"
        response = c.get(route)

        self.assertEquals(response.status_code, 200, "Database did not properly populate api")
