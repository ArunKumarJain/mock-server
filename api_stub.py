import json
from mockserver import MockServer

class ApiStub(MockServer):

    def __init__(self, host = "127.0.0.1", port = 5432):

        super().__init__(host = host, port = port)

    def onMobileModelInfo(self, **kwargs):

        # demonstrates how to read path segment parameter /mobiles/samsung/galaxy_a8
        print("Mobile manufacturer given: '{0}'".format(kwargs["manufacturer"]))
        print("Mobile model given: '{0}'".format(kwargs["model"]))

        priceJson = {"message": "unknown model"}
        # logic to return price based on manufacturer and model given
        if kwargs["manufacturer"].lower() == "samsung":
            if kwargs["model"].lower() == "galaxy_a8":
                priceJson = {"price": 52000}
            elif kwargs["model"].lower() == "galaxy_s9":
                priceJson = {"price": 54000}
        elif kwargs["manufacturer"].lower() == "apple":
            if kwargs["model"].lower() == "xs":
                priceJson = {"price": 104000}

        # default status code will be 200
        return json.dumps(priceJson)

    def onMobileManufacturerRequest(self, response = None, **kwargs):

        # getting response and returning it if that was set is just a demonstration to show that also we
        #  can do on top of call back
        if response:
            self.mobileManufacturerResponse = response

        # this is bit hacky again but can be used if it's really really needed
        # say if a specific test needs to return specific response which is not done in call back we can do like this
        if kwargs and hasattr(self, "mobileManufacturerResponse"):
            response = self.mobileManufacturerResponse
            del self.mobileManufacturerResponse
            return json.dumps(response["message"]), response["code"]

        return json.dumps(["samsung", "apple", "mi"])

    def onSearchRequest(self, **kwargs):

        # demonstrates how to read url params /mobiles?search=samsung
        search = kwargs.get('request').args.get("q")
        models = []
        if search.lower() == "samsung":
            models = [{"model": "galaxy_a8", "price": 52000}, {"model": "galaxy_s9", "price": 54000}]
        elif search.lower() == "apple":
            models = [{"model": "xs", "price": 104000}, {"model": "xr", "price": 88000}]

        # default status code will be 200
        return json.dumps(models)

    def onMobilesPost(self, **kwargs):

        print("Request body: ", kwargs.get('request').get_json())
        code = 201
        return json.dumps({"message": "successfully created"}), code

    def bad_request(self, **kwargs):

        code = 400
        msg = {"message": "error message"}
        return json.dumps(msg), code

    def initialise(self):

        # putting this code inside run() doesn't work
        # requires callback function to prepare response which needs to be returned
        self.add_callback_response(url = "/mobiles/<manufacturer>/<model>", callback = self.onMobileModelInfo,
                                   methods = ["GET"])

        self.add_callback_response(url = "/mobiles/manufacturers", callback = self.onMobileManufacturerRequest,
                                   methods = ["GET"])

        self.add_callback_response(url = "/mobiles", callback = self.onSearchRequest, methods = ["GET"])

        self.add_callback_response(url = "/mobiles", callback = self.onMobilesPost, methods = ["post"])
        self.add_callback_response(url = "/tablets", callback = self.bad_request)


if __name__ == '__main__':

    stubServer = ApiStub(host = "127.0.0.1", port = 5431)
    stubServer.daemon = True
    stubServer.start()

    # initialise all callback methods and routes here...
    stubServer.initialise()
    import time

    try:
        while True:
            time.sleep(3)
    except:
        stubServer.shutdown_server()