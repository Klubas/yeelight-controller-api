import os
import logging
from flask import request
from flask_restful import Resource
from flask import render_template, make_response

from .LightController import LightController

lights = LightController()
bulb_names = lights.get_bulb_names()


class Index(Resource):
    @staticmethod
    def get():
        headers = {
        	'Content-Type': 'text/html',
        	'Access-Control-Allow-Origin': '*'
        }

        html = os.path.join('index.html')
        return make_response(render_template(html), 200, headers)


class Bulb(Resource):
    @staticmethod
    def post():
        json = request.get_json(force=True)

        logging.debug(json)

        bulb_name = json['name'] if 'name' in json else None
        action = json['action'] if 'action' in json else None
        params = json['params'] if 'params' in json else None

        status = lights.run_action(
            name=bulb_name
            , action=action
            , params=params
        )

        print(status)

        return {'Response': status}, 200
