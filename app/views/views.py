import os
import json
from flask import request
from flask_restful import Resource, reqparse
from flask import render_template, make_response
from app.models.models import BulbController

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
        try:
            bulbs.__sync_bulbs__()
            response = bulbs.get_bulbs(metadata=True)
            response = json.dumps(str(response))
        except Exception as e:
            return {'Response': str(e)}, 500
        return {'Response': response}, 200


class Bulb(Resource):
    @staticmethod
    def get():
        """
        Get bulb metadata by ip
        :return:
        """
        try:

            parser = reqparse.RequestParser()
            parser.add_argument('ip', type=str, required=True, help='Bulb IP Adress')
            args = parser.parse_args()

            bulb_ip = args.ip

            response = bulbs.get_bulbs(ip=bulb_ip, metadata=True)
            response = json.dumps(str(response))
        except Exception as e:
            return {'Response': str(e)}, 500
        return {'Response': response}, 200

    @staticmethod
    def put():
        """
        Update bulb name
        :return:
        """
        return {'Response': "Not defined."}, 200


class Power(Resource):
    @staticmethod
    def post():
        """
        Change power state of bulb by IP
        If bulb <name> received will loop through all bulbs.
        :return:
        """
        try:

            parser = reqparse.RequestParser()
            parser.add_argument('ip', type=str, required=True, help='Bulb IP Adress')
            parser.add_argument('state', type=str, required=False, help='New power state. Toggle if not supplied.')
            args = parser.parse_args()

            bulb_ip = args.ip
            state = args.state if args.state else 'toggle'
            status = bulbs.power(ip=bulb_ip, state=state)

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
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('ip', type=str, required=True, help='Bulb IP Adress')
            args = parser.parse_args()
            bulb_ip = args.ip

            payload = request.get_json(force=True)
            color_mode = payload['mode'] if 'mode' in payload else None

            if not type:
                raise Exception("Field 'mode' is required ([rgb], hsv, bright, temp).")

            color_values = payload['values'] if 'values' in payload else None

            if not color_values:
                raise Exception("Field 'values' is required")

            values = list()

            if 0 < len(color_values) < 4:
                first_value = color_values[0]
                values.append(first_value)
                if len(color_values) >= 2:
                    second_value = color_values[1]
                    values.append(second_value)
                    if len(color_values) == 3:
                        third_value = color_values[2]
                        values.append(third_value)
            else:
                raise Exception("Invalid 'values': {}.".format(values))

            status = bulbs.change_color(ip=bulb_ip, values=tuple(values), color_mode=color_mode)

            return {'Response': str(status)}, 200

        except Exception as e:
            return {'Response': str(e)}, 500

    @staticmethod
    def get():
        """
        get bulb current color by ip
        :return:
        """
        return {'Response': "Not defined."}, 200
