from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from yw_db.models import Workflow

# Create your tests here.
class YwSaveTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_yw_ping(self):
        route = '/save/ping/'
        response = self.client.get(path=route)
        self.assertEqual(response.status_code, 200, msg="Valid route failed")

        bad_route = '/save/pig/'
        bad_response = self.client.get(path=bad_route)
        self.assertNotEqual(bad_response.status_code, 200, msg="Invalid route failed")

    def test_save_upload(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        route = '/save/'

        data = {}
        data['username'] = 'testuser'
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
