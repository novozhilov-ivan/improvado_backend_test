from flask import Flask
from flask_restful import Api


app = Flask('GeoName')
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json"
app.config["DEBUG"] = True
app.config["TESTING"] = True
app.config["FLASK_ENV"] = "development"
app.config["SERVER_NAME"] = "127.0.0.1:8000"
api = Api(app)


# api.add_resource(FindCities, "/api/cities/<int:geo_name_id>")
# api.add_resource(PageWithCities, "/api/cities/")
# api.add_resource(TwoRuCities, "/api/cities/<first_ru_geo_obj>&<second_ru_geo_obj>")
# api.add_resource(PartCityNameSearch, "/api/cities/search/<part_city_name>")
api.init_app(app)
