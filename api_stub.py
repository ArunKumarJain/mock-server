import json

class ApiStub():

    def __init__(self):
        pass

    def mobile_price(self, **kwargs):

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

    def search(self, **kwargs):

        # demonstrates how to read url params /mobiles?search=samsung
        search = kwargs.get('request').args.get("q")
        models = []
        if search.lower() == "samsung":
            models = [{"model": "galaxy_a8", "price": 52000}, {"model": "galaxy_s9", "price": 54000}]
        elif search.lower() == "apple":
            models = [{"model": "xs", "price": 104000}, {"model": "xr", "price": 88000}]

        # default status code will be 200
        return json.dumps(models)

    def post(self, **kwargs):

        print("Request body: ", kwargs.get('request').get_json())
        code = 201
        return json.dumps({"message": "successfully created"}), code

    def bad_request(self, **kwargs):

        code = 400
        msg = {"message": "error message"}
        return json.dumps(msg), code