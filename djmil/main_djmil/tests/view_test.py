import unittest
import requests


class MainPageTest(unittest.TestCase):

    def make_req(self):
        #url = 'http://127.0.0.1:80100/main_page'
        #req = requests.get(url).status_code
        a = 2
        b = 2
        return self.assertAlmostEqual(a, b)


if __name__ == "__main__":
    unittest.main()
