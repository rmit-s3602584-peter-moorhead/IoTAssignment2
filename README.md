# IoTAssignment2

Installation:

clone repo
copy setup.py to same level as repo folder
copy credentials.json to same level as repo folder
copy token.pickle to same level as repo folder
python3 -m venv venv
. venv/bin/activate
pip3 install flask
pip3 install flask-mysqldb
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
export FLASK_APP=IoTAssignment2
pip install -e .
flask run --host=0.0.0.0:5000
