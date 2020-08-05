import logging
from flask import request
from flask_restful import Resource

from server.LightController import LightController

lights = LightController()
bulb_names = lights.get_bulb_names()


class Index(Resource):
    @staticmethod
    def get():
        return {'Status': 'OK'}, 200


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

        return {'Response': status}, 200
