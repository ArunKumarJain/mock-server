# mock-server
  It's a standalone application that allows other systems to send the requests to it and responds with the pre-defined set of data or dynamically created data. 
  
  Most of the web applications communicate with external services/APIs almost at every request. During the QA to minimise the external dependencies or to simulate the external services failures we can use mock servers. In short make the external services behave the way we want. The main use cases are,

* Isolate the service to be tested by using mock server for other integration services
* Speed up the testing by mocking slow external services
* Avoid calling expensive 3rd party external services 
* Validate the requests sent by the system under test to the external services 

### Work flow:

1. Start the mock server and register the URLs we wanted to handle and set response that should be returned when hitting the URLs. This can be achieved in two ways,

  * add_response_json
  
  mockserver.add_response_json(url = "/mobiles/manufacturers", serializable = ["lg", "apple", "samsung"], methods = ("GET",))

  ![picture alt](https://github.com/ArunKumarJain/mock-server/images/add_response_json.png)
   
   * add_response_callback

  mockserver.add_response_callback(url = "/mobiles/manufacturers", callback = callbackMethod, methods = ("GET",))

  ![picture alt](https://github.com/ArunKumarJain/mock-server/images/add_callback_functions.png)

2. Replace the external service URL with the mock server URL in the service that is under test so that requests will come to mock server instead of the external service 

3. Mock server will now receive the requests and tries to understand whether it can respond to it (and if yes with what data). We can specify each and every aspect of the response – from HTTP code to headers and body. If the URL is not registered it will respond 404

### Steps to execute tests

* Checkout the code to a local folder
* Install modules in requirements.txt<br>
* Run tests using command "python tests/test_add_response_json.py" or "python tests/test_callback_function.py"
