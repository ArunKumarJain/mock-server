import unittest
import requests
import json
from api_stub import ApiMock
import time

class TestMockServer(unittest.TestCase):

    def setUp(self):

        self.server = ApiMock(host = "localhost", port = 5001)

    def test_url_params(self):

        # demonstrate how to create a stub for get API and without a callback function
        # static responses for specific routes can be done like this

        response = requests.get(self.server.url + "/mobiles?q=samsung")
        self.assertEqual(200, response.status_code)
        self.assertEqual([{'model': 'galaxy_a8', 'price': 52000}, {'model': 'galaxy_s9', 'price': 54000}], response.json())

        # demonstrating on how to set response & code from test
        resp = [{'model': 'galaxy_a7', 'price': 19000}, {'model': 'galaxy_s9+', 'price': 24000}]
        self.server.onSearchRequest(response = {"message": resp, "code": 200})
        response = requests.get(self.server.url + "/mobiles?q=samsung")
        self.assertEqual(resp, response.json())
        self.assertEqual(200, response.status_code)

        # resetting the response set
        self.server.onSearchRequest(response = None)

        # demonstrating on how to set callbackFunction for a method
        def onSearchRequestCallback(**kwargs):

            search = kwargs.get('request').args.get("q")
            models = []
            if search.lower() == "samsung":
                models = [{"model": "j7", "price": 80000}, {"model": "j6", "price": 9000}]
            elif search.lower() == "apple":
                models = [{"model": "6", "price": 12000}, {"model": "6+", "price": 14000}]

            return json.dumps(models), 200

        self.server.onSearchRequest(callback_func = onSearchRequestCallback)
        response = requests.get(self.server.url + "/mobiles?q=apple")
        self.assertEqual([{"model": "6", "price": 12000}, {"model": "6+", "price": 14000}], response.json())
        self.assertEqual(200, response.status_code)

        # resetting the callback_func set
        self.server.onSearchRequest(callback_func = None)

    def test_url_segement_params(self):

        # demonstrate how to create a stub for get API and read the path segment parameters
        # response based on the parameters can be generated in callback function

        response = requests.get(self.server.url + "/mobiles/samsung/galaxy_a8")
        self.assertEqual({"price": 52000}, response.json())

        # demonstrating on how to set response & code from test
        resp = {"price": 12000}
        self.server.onMobileModelInfo(response = {"message": resp, "code": 200})
        response = requests.get(self.server.url + "/mobiles/samsung/j7")
        self.assertEqual(resp, response.json())
        self.assertEqual(200, response.status_code)

        # resetting the response set
        self.server.onMobileModelInfo(response = None)

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