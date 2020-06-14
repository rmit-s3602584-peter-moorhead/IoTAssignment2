# Internet of Things Assignment 2
###### Peter, Tim, Taylor, Joel
## Car Rental Service

This repo aims to solve the assignment 3 of Internet of Things describing a car rental system
hosted on a raspberry pi and accessed through a combination of a Flask webapp and API.
Users will be able to register an account and login.
Search Cars available for hire
Make bookings and link their google calendar to tell them when they have their car
Cancel existing bookings if need be

# Logins
* Username: admin1, Password: admin1
* Username: Engineer1, Password: Engineer1
* Username: Manager1, Password: Manager1



##### Installation:

clone repo
copy setup.py to same level as repo folder
copy credentials.json to same level as repo folder
copy token.pickle to same level as repo folder
```bash
python3 -m venv venv
. venv/bin/activate
(venv) pip3 install flask
(venv) pip3 install flask-mysqldb
(venv) pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
(venv) export FLASK_APP=IoTAssignment2
(venv) pip install -e .
(venv) flask run --host=0.0.0.0
```
