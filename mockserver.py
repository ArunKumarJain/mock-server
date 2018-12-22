import requests
from flask import jsonify, Flask, request
from threading import Thread

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

    def add_callback_response(self, url, callback, methods = ('GET',)):

        self.app.add_url_rule(rule = url, view_func = callback, defaults = {"request": request}, methods = methods)

    def add_json_response(self, url, serializable, methods = ('GET',)):

        def callback(**kwargs):
            return jsonify(serializable)

        self.add_callback_response(url = url, callback = callback, methods = methods)

    def run(self):

        self.app.run(host = self.host, port = self.port)