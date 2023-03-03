from flask_restful import Resource, reqparse
from flask import jsonify

from api.keys import client_secret_key

parser = reqparse.RequestParser()

parser.add_argument(
    'code',
    type=str,
    location='args'
)


class Code(Resource):
    @staticmethod
    def get():
        args = parser.parse_args()
        code = args['code']
        # path = "access_token"
        # client_id = '51571106'  # идентификатор приложения.
        # scheme = 'https'
        # authority = 'oauth.vk.com'
        # redirect_page = "127.0.0.1:8000/api/auth/"
        # url_get_access_token = f"{scheme}://{authority}/{path}?" \
        #                        f"client_id={client_id}&" \
        #                        f"client_secret={secret_key}&" \
        #                        f"redirect_uri={redirect_page}&" \
        #                        f"code={code}"
        return jsonify(**args)
