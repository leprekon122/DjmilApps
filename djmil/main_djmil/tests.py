"""import pickets """
from __future__ import absolute_import
from unittest import TestCase
import requests
from datetime import datetime
from main_djmil.models import SecondOrdersModel


class TestMainPage(TestCase):
    """test login page"""

    def test_get_request(self):
        """test get req  in login page"""
        req = requests.get("http://127.0.0.1:8000", timeout=10).status_code
        return self.assertEqual(req, 200)

    def test_login_func(self):
        """test login funct"""
        req = requests.post("http://127.0.0.1:8000", timeout=10).status_code
        return self.assertEqual(req, 403)


class TestOnlineSecondOrders(TestCase):
    """class for testing (online_second_order) page"""

    def test_make_get_req(self):
        """test get req"""
        req = requests.get("http://127.0.0.1:8000/online_second_orders/", timeout=10).status_code
        return self.assertEqual(req, 403)


class TestOnlineSecondModel(TestCase):
    """testing SecondOrdersModel"""

    def setUp(self) -> None:
        SecondOrdersModel.objects.create(serial_no=123456, product_type=67, longitude=0.00000,
                                         latitude=0.000000, dt=datetime.today(),
                                         phone_app_latitude=0.000000,
                                         phone_app_longitude=0.000000, phone_app_x=0.0000000,
                                         phone_app_y=0.000000,
                                         home_latitude=0.0000000, home_longitude=0.00000000,
                                         home_x=0.000000, home_y=0.000000
                                         )

    def test_create_data(self):
        """make create method"""
        serial_no = SecondOrdersModel.objects.get('serial_no')

        return self.assertEqual(serial_no, 123456)


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
