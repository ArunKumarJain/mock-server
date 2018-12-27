import unittest
import requests
import json
from api_stub import ApiStub
import time

class TestMockServer(unittest.TestCase):

    def setUp(self):

        self.server = ApiStub(host = "localhost", port = 5001)
        self.server.daemon = True
        self.server.start()
        self.server.initialise()

        # adding little sleep as start & shutdown mock server very often creates
        # connection problems
        time.sleep(0.25)

    def test_url_params(self):

        # demonstrate how to create a stub for get API and without a callback function
        # static responses for specific routes can be done like this

        response = requests.get(self.server.url + "/mobiles?q=samsung")
        self.assertEqual(200, response.status_code)
        # self.assertIn('mobiles', response.json())
        # self.assertEqual(["samsung", "apple"], response.json()['mobiles'])

    def test_url_segement_params(self):

        # demonstrate how to create a stub for get API and read the path segment parameters
        # response based on the parameters can be generated in callback function

        response = requests.get(self.server.url + "/mobiles/samsung/galaxy_a8")
        self.assertEqual({"price": 52000}, response.json())

    def test_post_read_request_body(self):

        # demonstrate how to create a stub for post API and read the json sent in request body
        jsonBody = [{"manufacturer": "red-mi", "models": [{"model": "a8", "price": "16000"},
                                                          {"model": "6pro", "price": "11000"}]}]

        response = requests.post(self.server.url + "/mobiles", json = jsonBody)
        self.assertEqual(201, response.status_code)
        self.assertEqual({"message": "successfully created"}, response.json())

    def test_bad_request(self):

        response = requests.get(self.server.url + "/tablets")
        self.assertEqual(400, response.status_code)
        # intentionally creating a assertion failure
        self.assertEqual({"message": "error message"}, response.json())

    def tearDown(self):

        self.server.shutdown_server()

if __name__ == '__main__':
    unittest.main()