import os
import secrets
from dotenv import load_dotenv
from flask_restful import Resource
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from api.models.ResponseHandler import ResponseHandler as Handler, APIStatus

load_dotenv()

auth = HTTPTokenAuth(scheme='Bearer')


tokens = {
    secrets.token_hex(16):
        (os.getenv('YC_USERNAME'), generate_password_hash(os.getenv('YC_PWD')))
}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


class Token(Resource):
    decorators = [auth.login_required]

    @staticmethod
    def get():
        """
        Return tokens
        :return:
        """
        return Handler.exception(
            status=APIStatus.METHOD_NOT_DEFINED,
            params=None
        )

    @staticmethod
    def post():
        """
        Create new token
        :return:
        """
        return Handler.exception(
            status=APIStatus.METHOD_NOT_DEFINED,
            params=None
        )

    @staticmethod
    def put():
        """
        Update current Token
        :return:
        """
        return Handler.exception(
            status=APIStatus.METHOD_NOT_DEFINED,
            params=None
        )


login = HTTPBasicAuth()


@login.verify_password
def verify_password(username, password):
    token = None
    for item in tokens.items():
        if username == item[1][0] \
                and check_password_hash(item[1][1], password):
            token = item[0]
            break
    if token:
        new_token = secrets.token_hex(16)
        tokens[new_token] = tokens.pop(token)
        return new_token


class Logon(Resource):
    decorators = [login.login_required]

    @staticmethod
    def post():
        """
        Return token for specified user:password
        :return:
        """
        return Handler.success(response=login.current_user())
