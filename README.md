# Client Wrapper
###### _Created using Python and Django_
Goal: to create a client wrapper that would handle file upload to the endpoint servers.

### Installation

The client requires django and python installed to run. 
Specifically, it also requires the python requests module.
Install the dependencies and start the server.

It would be easier to set up the project in a virtual environment:
```sh
cd bynder_wrapper
python -m venv venv
.\venv\Scripts\activate
```

Add django dependencies:
```sh
python -m pip install django==4.1.3
```

You may need  to install python's requests module:
```sh
python -m pip install requests
```

To run the development web server:
```sh
python manage.py runserver
```

The server at http://localhost:8000/ should now display an upload form where you can upload a test file and test token. 

The code that creates the wrapper is located in `bynder_wrapper/cwrapper/views.py` 

#### _Answers to additional questions_

#### 1. What happens if there is an internal server problem?
> If a problem occurs during upload, one way to potentially handle this would be to add a condition that checks for the status response of each upload. In python, calling the requests variable returns a status like 200 for OK or 500 for internal server error. We could trigger an email to the system to inform of a server error during upload, or we could send a request to a customer service API if it exists to notify them of server error. 

#### 2. What happens to the rest of the workflow if one of the chunks fails to upload?
> I initially designed the code with `try` / `except` blocks just so I could have something to display after form submission to visually ensure the necessary data in the workflow upload is passed accurately to the hypothetical endpoint. We could extend these blocks to returning a status message to display to the client if one of the chunks fails to return an appropriate response. 

#### 3. How would you turn this into a batch flow upload?
> To transform a single upload function into a batch upload, we would have to make use of multiprocessing and threading to turn this single loop into a series that can run in parallel. Python has some built-in libraries for this such as `joblib` and `pathos`. And then to ensure that overhead computation cost isn't too high, we would probably have to create an additional wrapper function that works on the batch instead of serializing each item.
