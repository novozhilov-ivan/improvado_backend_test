from flask import Flask

app = Flask('VK_get_friends_report', template_folder='app/templates')
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json"
app.config["DEBUG"] = True
app.config["TESTING"] = True
app.config["FLASK_ENV"] = "development"
app.config["SERVER_NAME"] = "127.0.0.1:8000"
