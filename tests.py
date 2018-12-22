import unittest
import requests
import json
from mockserver import MockServer
from api_stub import ApiStub

class TestMockServer(unittest.TestCase):

    def setUp(self):

        self.server = MockServer(host = "localhost", port = 5001)
        self.server.daemon = True
        self.server.start()
        self.apiStub = ApiStub()

    def test_mock_with_json_serializable(self):

        # demonstrate how to create a stub for get API and without a callback function
        # static responses for specific routes can be done like this

        self.server.add_json_response(url = "/mobiles", serializable = dict(mobiles = ["samsung", "apple"]))
        response = requests.get(self.server.url + "/mobiles")
        self.assertEqual(200, response.status_code)
        self.assertIn('mobiles', response.json())
        self.assertEqual(["samsung", "apple"], response.json()['mobiles'])

    def test_mock_with_callback(self):

        # demonstrate how to create a stub for get API and read the path segment parameters
        # response based on the parameters can be generated in callback function

        self.server.add_callback_response(url = "/mobiles/<manufacturer>/<model>", callback = self.apiStub.mobile_price)
        response = requests.get(self.server.url + "/mobiles/samsung/galaxy_a8")
        self.assertEqual({"price": 52000}, response.json())

    def test_read_request_body(self):

        # demonstrate how to create a stub for post API and read the json sent in request body
        self.server.add_callback_response(url = "/mobiles", callback = self.apiStub.post, methods = ["post"])
        jsonBody = [{"manufacturer": "red-mi", "models": [{"model": "a8", "price": "16000"},
                                                          {"model": "6pro", "price": "11000"}]}]

        response = requests.post(self.server.url + "/mobiles", json = jsonBody)
        self.assertEqual(201, response.status_code)
        self.assertEqual({"message": "successfully created"}, response.json())

    def test_bad_request(self):

        self.server.add_callback_response(url = "/tablets", callback=self.apiStub.bad_request)

        response = requests.get(self.server.url + "/tablets")
        self.assertEqual(400, response.status_code)
        # intentionally creating a assertion failure
        self.assertEqual({"message": "error message"}, response.json())


    def tearDown(self):

        self.server.shutdown_server()

if __name__ == '__main__':
    unittest.main()