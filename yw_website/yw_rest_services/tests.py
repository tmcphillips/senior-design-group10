from django.test import TestCase
from django.test.client import Client

# Create your tests here.
class YwSaveTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_yw_ping(self):
        route = '/save/ping/'
        response = self.client.get(path=route)
        self.assertEqual(response.status_code, 200, msg="Valid route failed")

        bad_route = '/save/pig'
        bad_response = self.client.get(path=bad_route)
        self.assertNotEqual(bad_response.status_code, 200, msg="Invalid route failed")
