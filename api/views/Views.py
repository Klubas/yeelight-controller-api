import os
import logging, traceback
from flask_restful import Resource, reqparse
from flask import render_template, make_response
from api.models.BulbController import BulbController
from api.views.ResponseHandler import ResponseHandler, APIStatus, APIMessage

handler = ResponseHandler()
bulbs = BulbController()


class Index(Resource):
    @staticmethod
    def get():
        headers = {
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*'
        }

        html = os.path.join('index.html')
        return make_response(
            render_template(html), 200, headers)


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
            return handler.success(response=response)
        except Exception as e:
            logging.exception(APIStatus.ERROR.value.get('message'))
            return handler.exception(
                status=APIStatus.ERROR,
                exception=e,
                traceback=traceback.format_exc(),
                params=None
            )


class Bulb(Resource):
    @staticmethod
    def get():
        """
        Get bulb metadata by ip
        :return:
        """
        return_status = APIStatus.ERROR
        parser = reqparse.RequestParser()
        parser.add_argument('ip', type=str, required=True,
                            help=APIStatus.IP_REQUIRED.value.get('message'))
        parser.add_argument('property', type=str, required=False,
                            help='Returns a bulb property')
        args = parser.parse_args()

        try:
            bulbs.__sync_bulbs__()
            response = bulbs.get_bulbs(ip=args.ip, metadata=True)

            if len(response) > 0:
                response = response[0]
            else:
                return_status = APIStatus.BULB_NOT_FOUND
                raise Exception("Bulb {} was not found in the network.".format(args.ip))

            if args.property:
                if args.property in response.keys():
                    response = response[args.property]
                elif args.property in response['properties'].keys():
                    response = response['properties'][args.property]
                else:
                    return_status = APIStatus.VALUE_ERROR
                    raise Exception(APIMessage.VALUE_ERROR_ARG.value.get('message').format(args.property, 'property'))
            return handler.success(response={args.property: response})
        except Exception as e:
            logging.exception(return_status.value.get('message'))
            return handler.exception(
                status=return_status,
                params=args,
                traceback=traceback.format_exc(),
                exception=e
            )

    @staticmethod
    def put():
        """
        Update bulb name
        :return:
        """
        return_status = APIStatus.ERROR
        parser = reqparse.RequestParser()
        parser.add_argument('ip', type=str, required=True,
                            help=APIStatus.IP_REQUIRED.value.get('message'))
        parser.add_argument('new_name', type=str, required=True,
                            help=APIMessage.REQUIRED_ARG.value.get('message')
                            .format('new_name', None))
        args = parser.parse_args()

        try:
            status = bulbs.rename_bulb(ip=args.ip, new_name=args.new_name)
            return handler.success(response=status)
        except Exception as e:
            logging.exception(APIStatus.ERROR.value.get('message'))
            return handler.exception(
                status=return_status,
                exception=e,
                traceback=traceback.format_exc(),
                params=args
            )


class Power(Resource):
    @staticmethod
    def post():
        """
        Change power state of bulb by IP
        If bulb <name> received will loop through all bulbs.
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('ip', type=str, required=True,
                            help=APIStatus.IP_REQUIRED.value.get('message'))
        parser.add_argument('state', type=str, required=False,
                            help=APIMessage.REQUIRED_ARG.value.get('message')
                            .format('state', 'on, off, toggle'))

        args = parser.parse_args()

        args.state = args.state if args.state else 'toggle'

        try:
            status = bulbs.power(ip=args.ip, state=args.state)
            return handler.success(response=status)
        except Exception as e:
            logging.exception(APIStatus.ERROR.value.get('message'))
            return handler.exception(
                status=APIStatus.ERROR,
                params=args,
                traceback=traceback.format_exc(),
                exception=e)


class Color(Resource):
    @staticmethod
    def post():
        """
        Change bulb current color by ip
        :return:
        """
        parser = reqparse.RequestParser()

        parser.add_argument('ip', type=str, required=True,
                            help=APIStatus.IP_REQUIRED.value.get('message'))

        parser.add_argument('mode', dest='color_mode', type=str, required=True, location=['json', 'values'],
                            help=APIMessage.REQUIRED_ARG.value.get('message')
                            .format('mode', 'rgb, hsv, bright, temp'))

        parser.add_argument('values', dest='color_values', action='append', type=int, required=True, location=['json', 'values'],
                            help=APIMessage.REQUIRED_ARG.value.get('message')
                            .format('values', '[<int>, [int], [int]]'))

        args = parser.parse_args()

        try:
            status = bulbs.change_color(ip=args.ip, values=tuple(args.color_values), color_mode=args.color_mode)
            return handler.success(response=status)
        except Exception as e:
            logging.exception(APIStatus.ERROR.value.get('message'))
            return handler.exception(
                status=APIStatus.ERROR,
                params=args,
                traceback=traceback.format_exc(),
                exception=e
            )
