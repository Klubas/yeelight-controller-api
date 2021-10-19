import os
import secrets
from datetime import datetime, timedelta
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
env_local_token = os.getenv('YC_LOCAL_TOKEN')

if not env_username or not env_password:
    raise Exception("Environment variables not set in .env\n{}".format('YC_USERNAME, YC_PWD'))
else:
    env_password = generate_password_hash(env_password)
    tokens = {
        secrets.token_hex(16):
            (env_username, env_password, datetime.now())
    }

    if env_local_token:
        tokens[env_local_token] = (
            secrets.token_hex(16)
            , secrets.token_hex(16)
            , datetime.now()
        )


def allow_local_access():
    from flask import request
    req_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    req_ip.replace('localhost', '127.0.0.1')

    ip_range = req_ip.split('.')
    ip_range = ip_range[0] + '.' + ip_range[1]

    if ip_range in ('127.0', '0.0', '192.168'):
        return True
    return False


@auth.verify_token
def verify_token(token):
    if token in tokens:

        username = tokens[token][0]
        if env_local_token:
            if allow_local_access():
                return username

        expiration_date = tokens[token][2] + timedelta(days=3)
        expired = True if expiration_date > datetime.now() else False

        if not expired:
            return username


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
        tokens[new_token] = (tokens[new_token][0],
                             tokens[new_token][1],
                             tokens[new_token][2])
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
