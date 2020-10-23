
# Local development

* Set up virtual env `python3 -m venv /path/to/venv`
* Activate it: `source /apth/to/venv/bin/activate`
* Install requirements `pip install -r requirements.txt`

* Start the server locally:
** `export FLASK_APP=app.py`
** `export FLASK_ENV=development`
** `flask run [--port 8080]`