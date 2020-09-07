import os
from flask_restful import Resource
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):

    tokens = {
        os.getenv('YC_TOKEN'): os.getenv('YC_USERNAME'),
    }

    if token in tokens:
        return tokens[token]


class Logon(Resource):
    def post(self):
        """
        Return token for specified user:password
        :return:
        """
        pass


class Token(Resource):
    decorators = [auth.login_required]

    @staticmethod
    def get():
        """
        Return tokens
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
