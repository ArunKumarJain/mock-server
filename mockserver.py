import json
import requests
from flask import jsonify, Flask, request
from threading import Thread
import functools

class MockWrapper:

    def __init__(self, func):

        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):

        responseAttrName = "{0}Response".format(self.func.__name__)
        codeAttrName = "{0}ResponseCode".format(self.func.__name__)
        callbackFuncAttrName = "{0}CallbackFunc".format(self.func.__name__)

        if "response" in kwargs:
            if kwargs.get("response"):
                setattr(self, responseAttrName, kwargs.get("response").get("message", {}))
                setattr(self, codeAttrName, kwargs.get("response").get("code", 200))
            else:
                # if response is given as None delete the attr that was set
                delattr(self, responseAttrName)
                delattr(self, codeAttrName)

            return

        if "callback_func" in kwargs:
            if kwargs.get("callback_func"):
                setattr(self, callbackFuncAttrName, kwargs.get("callback_func"))
            else:
                # if callback_func is given as None delete the attr that was set
                delattr(self, callbackFuncAttrName)

            return

        if kwargs.get("request"):
            if hasattr(self, responseAttrName):
                return json.dumps(getattr(self, responseAttrName)), getattr(self, codeAttrName)
            if hasattr(self, callbackFuncAttrName):
                responseAttrName = getattr(self, callbackFuncAttrName)(*args, **kwargs)
                return responseAttrName

        return self.func(self, *args, **kwargs)

class MockServer(Thread):

    def __init__(self, host = "127.0.0.1", port = 5432):
        """
        Parameters:
            (str) host: give 0.0.0.0 to have server available externally. Default is 127.0.0.1
            (int) port: port of the Webserver. 5432
        """

        super().__init__()
        self.port = port
        self.host = host
        self.url = "http://{0}:{1}".format(host, port)
        self.app = Flask(__name__)
        self.app.add_url_rule("/shutdown", view_func = self._shutdown_server)

    def _shutdown_server(self):

        if not 'werkzeug.server.shutdown' in request.environ:
            raise RuntimeError('Not running the development server')
        request.environ['werkzeug.server.shutdown']()
        return 'Server shutting down...'

    def shutdown_server(self):

        requests.get("http://localhost:%s/shutdown" % self.port)
        self.join()

    def add_response_callback(self, url, callback, methods = ('GET',)):

        self.app.add_url_rule(rule = url, view_func = callback, defaults = {"request": request}, methods = methods)

    def add_response_json(self, url, serializable, methods = ('GET',)):

        def callback(**kwargs):
            return jsonify(serializable)

        self.add_response_callback(url = url, callback = callback, methods = methods)

    def run(self):

        self.app.run(host = self.host, port = self.port)