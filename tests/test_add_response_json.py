import unittest
import requests
import json
import sys
sys.path.append(".")
from mockserver import MockServer
import time

class TestMockServer(unittest.TestCase):

    def setUp(self):

        self.server = MockServer(host = "localhost", port = 5001)
        self.daemon = True
        self.server.start()

    def test_add_response_json(self):

        # example of how to add response json that needs to be returned for any requests for a specific route

        self.server.add_response_json(url = "/mobiles/manufacturers", serializable = ["samsung", "apple", "mi"],
                                      methods = ('GET',))

        response = requests.get(self.server.url + "/mobiles/manufacturers")
        self.assertEqual(200, response.status_code)
        self.assertEqual(["samsung", "apple", "mi"], response.json())

    def tearDown(self):

        self.server.shutdown_server()

if __name__ == '__main__':
    unittest.main()