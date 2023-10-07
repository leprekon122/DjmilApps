"""import pickets """
from unittest import TestCase
import requests


class TestMainPage(TestCase):
    """test login page"""

    def test_get_request(self):
        """test get req  in login page"""
        req = requests.get("http://127.0.0.1:8000", timeout=10).status_code
        return self.assertEqual(req, 200)

    def test_login_func(self):
        """test login funct"""
        req = requests.post("http://127.0.0.1:8000", timeout = 10).status_code
        return self.assertEqual(req, 403)


class TestOnlineSecondOrders(TestCase):
    """class for testing (online_second_order) page"""

    def test_make_get_req(self):
        """test get req"""
        req = requests.get("http://127.0.0.1:8000/online_second_orders/", timeout=10).status_code
        return self.assertEqual(req, 403)


class TestCombatOrderPage(TestMainPage):
    """test for CombatOrder page"""

    def test_make_get_req(self):
        """test get req"""
        req = requests.get("http://127.0.0.1:8000/combat_orders/", timeout=10).status_code
        return self.assertEqual(req, 403)


class TestStatisticsPage(TestCase):
    """Test for statistics page"""

    def test_make_get_req(self):
        """test get req"""
        req = requests.get("http://127.0.0.1:8000/statistics/", timeout=10).status_code
        return self.assertEqual(req, 403)
