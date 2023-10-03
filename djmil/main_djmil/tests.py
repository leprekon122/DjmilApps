from django.test import TestCase


# Create your tests here.
class TestLoginPage(TestCase):

    def test_requst_to_login_page(self):
        response = self.client.get('online_second_orders/')
        self.assertEqual(response.status_code, 200)

