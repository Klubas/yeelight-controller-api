import os
import logging
import json
from flask import request
from flask_restful import Resource, reqparse
from flask import render_template, make_response
from app.models.models import BulbController

"""
New methods
"""

bulbs = BulbController()


class Index(Resource):
    @staticmethod
    def get():
        headers = {
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*'
        }

        html = os.path.join('index.html')
        return make_response(render_template(html), 200, headers)


class Bulbs(Resource):
    @staticmethod
    def get():
        """
        Get list of bulbs metadata (ip, name, model, power state, color)
        :return:
        """
        response = bulbs.get_bulbs_metadata()
        response = json.dumps(response)
        return {'Response': response}, 200


class Power(Resource):
    @staticmethod
    def post():
        """
        Change power state of bulb by IP
        If bulb <name> received will loop through all bulbs.
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('ip', type=str, required=True, help='Bulb IP Adress')
        parser.add_argument('state', type=str, required=True, help='New power state')
        args = parser.parse_args()

        bulb_ip = args['ip']
        state = args['state']

        try:
            status = bulbs.power(bulb_ip=bulb_ip, state=state)
            return {'Response': str(status)}, 200
        except Exception as e:
            return {'Response': str(e)}, 500

    @staticmethod
    def get():
        """
        get bulb power current state
        On, Off, Null
        :return:
        """
        return {'Response': "Not defined."}, 200


class Color(Resource):
    @staticmethod
    def post():
        """
        Change bulb current color by ip
        :return:
        """
        return {'Response': "Not defined."}, 200

    @staticmethod
    def get():
        """
        get bulb current color by ip
        :return:
        """
        return {'Response': "Not defined."}, 200
