# IoTAssignment2

Installation:

clone repo
copy setup.py to same level as repo folder
copy credentials.json to same level as repo folder
copy token.pickle to same level as repo folder
python3 -m venv venv
. venv/bin/activate
(venv) pip3 install flask
(venv) pip3 install flask-mysqldb
(venv) pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
(venv) export FLASK_APP=IoTAssignment2
(venv) pip install -e .
(venv) flask run --host=0.0.0.0:5000
