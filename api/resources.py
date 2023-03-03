from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument(
    'scope',
    type=str,
    location='args'
)
parser.add_argument(
    'code',
    type=str,
    location='args'
)


class Code(Resource):
    @staticmethod
    def get():
        args = parser.parse_args()
        scope = args['scope']
        code = args['code']

        print(scope, code)
