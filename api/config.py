from flask import Flask
from flask_restful import Api

from api.resources import *

app = Flask('VK_get_friends_report')
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json"
app.config["DEBUG"] = True
app.config["TESTING"] = True
app.config["FLASK_ENV"] = "development"
app.config["SERVER_NAME"] = "127.0.0.1:8000"
api = Api(app)


api.add_resource(Code, '/api/')
api.init_app(app)
