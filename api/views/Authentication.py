import os
import secrets
from datetime import datetime
from dotenv import load_dotenv
from flask_restful import Resource
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from api.models.ResponseHandler import ResponseHandler as Handler, APIStatus

load_dotenv()

auth = HTTPTokenAuth(scheme='Bearer')
login = HTTPBasicAuth()

env_username = os.getenv('YC_USERNAME')
env_password = os.getenv('YC_PWD')

if env_username and env_password:
    env_password = generate_password_hash(env_password)
    tokens = {
        secrets.token_hex(16):
            (env_username, env_password, datetime.now())
    }
else:
    raise Exception("Environment variables not set in .env\n{}".format('YC_USERNAME, YC_PWD'))


@auth.verify_token
def verify_token(token):
    if token in tokens:
        expiration_date = None if tokens[token][2] else None #implementar logica
        if expiration_date:
            return tokens[token][0]
        else:
            return tokens[token][0]


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
        tokens[new_token] = (username, password, datetime.now())
        return new_token
    else:
        return ''


class Logon(Resource):
    decorators = [login.login_required]

    @staticmethod
    def post():
        """
        Return token for specified user:password
        :return:
        """
        print(login.current_user())
        if login.current_user() != '':
            return Handler.success(
                response=login.current_user(),
                status=APIStatus.LOGIN_SUCCESS
            )
        else:
            return Handler.exception(
                status=APIStatus.LOGIN_ERROR,
                params=None
            )
