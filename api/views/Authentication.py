import os
from flask_restful import Resource
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    
    tokens = {
        os.getenv('YEELIGHT_TOKEN'): os.getenv('YEELIGHT_USERNAME'),
    }

    if token in tokens:
        return tokens[token]


class Token(Resource):
    decorators = [auth.login_required]

    @staticmethod
    def get():
        """
        Return all tokens
        :return:
        """
        pass

    @staticmethod
    def post():
        """
        Create new token
        :return:
        """
        pass

    @staticmethod
    def put():
        """
        Update current Token
        :return:
        """
        pass
