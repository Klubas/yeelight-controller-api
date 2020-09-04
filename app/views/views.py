import os
import logging
import json
from flask import request
from flask_restful import Resource
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
        payload = request.get_json(force=True) # payload must be a list of objects

        bulb_ip = payload['action'] if 'action' in payload else None
        state = payload['params'] if 'params' in payload else None

        status = bulbs.power(bulb_ip=bulb_ip, state=state)

        return {'Response': str(status)}, 200

    @staticmethod
    def get():
        """
        get bulb power current state
        On, Off, Null
        :return:
        """
        return {'Response': "Not defined."}


class Color(Resource):
    @staticmethod
    def post():
        """
        Change bulb current color by ip
        :return:
        """
        return {'Response': "Not defined."}

    @staticmethod
    def get():
        """
        get bulb current color by ip
        :return:
        """
        return {'Response': "Not defined."}

"""
OLD Methods
"""
from app.models.modelsOLD import BulbController as BulbControllerOLD

lights = BulbControllerOLD()
bulb_names = lights.get_bulb_names()


class Bulb(Resource):
    @staticmethod
    def post():
        payload = request.get_json(force=True)

        logging.debug(payload)

        bulb_name = payload['name'] if 'name' in payload else None
        action = payload['action'] if 'action' in payload else None
        params = payload['params'] if 'params' in payload else None

        status = lights.run_action(
            name=bulb_name
            , action=action
            , params=params
        )

        return {'Response': status}, 200
