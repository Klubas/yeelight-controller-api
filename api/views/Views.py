import os
import logging, traceback
from flask_restful import Resource, reqparse
from flask import render_template, make_response, request
from api.models.BulbController import BulbController
from api.views.ResponseHandler import ResponseHandler, APIStatusMessage

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
            return handler.return_success(status=response)
        except Exception as e:
            logging.exception(APIStatusMessage.ERROR.value[0])
            return handler.return_exception(
                status=APIStatusMessage.ERROR,
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
        parser = reqparse.RequestParser()
        parser.add_argument('ip', type=str, required=True,
                            help=APIStatusMessage.IP_REQUIRED.value[0])
        args = parser.parse_args()

        try:
            response = bulbs.get_bulbs(ip=args.ip, metadata=True)
            response = response[0]
            return handler.return_success(status=response)

        except Exception as e:
            logging.exception(APIStatusMessage.ERROR.value[0])
            return handler.return_exception(
                status=APIStatusMessage.ERROR,
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

        parser = reqparse.RequestParser()
        parser.add_argument('ip', type=str, required=True,
                            help=APIStatusMessage.IP_REQUIRED.value[0])
        parser.add_argument('new_name', type=str, required=True,
                            help=APIStatusMessage.REQUIRED_ARG.value[0]
                            .format('new_name', None))
        args = parser.parse_args()

        try:
            status = bulbs.rename_bulb(ip=args.ip, new_name=args.new_name)
            return handler.return_success(status=status)
        except Exception as e:
            logging.exception(APIStatusMessage.ERROR.value[0])
            return handler.return_exception(
                status=APIStatusMessage.ERROR,
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
                            help=APIStatusMessage.IP_REQUIRED.value[0])
        parser.add_argument('state', type=str, required=False,
                            help=APIStatusMessage.IP_REQUIRED.value[0]
                            .format('state', 'on, off, toggle'))

        args = parser.parse_args()

        args.state = args.state if args.state else 'toggle'

        try:
            status = bulbs.power(ip=args.ip, state=args.state)
            return handler.return_success(status=status)
        except Exception as e:
            logging.exception(APIStatusMessage.ERROR.value[0])
            return handler.return_exception(
                status=APIStatusMessage.ERROR,
                params=args,
                traceback=traceback.format_exc(),
                exception=e)

    @staticmethod
    def get():
        """
        get bulb power current state
        On, Off, Null
        :return:
        """

        return handler.return_exception(
            status=APIStatusMessage.METHOD_NOT_DEFINED,
            params=None
        )


class Color(Resource):
    @staticmethod
    def post():
        """
        Change bulb current color by ip
        :return:
        """
        parser = reqparse.RequestParser()

        parser.add_argument('ip', type=str, required=True,
                            help=APIStatusMessage.IP_REQUIRED.value[0])

        parser.add_argument('mode', dest='color_mode', type=str, required=True, location=['json', 'values'],
                            help=APIStatusMessage.REQUIRED_ARG.value[0]
                            .format('mode', 'rgb, hsv, bright, temp'))

        parser.add_argument('values', dest='color_values', action='append', type=int, required=True, location=['json', 'values'],
                            help=APIStatusMessage.REQUIRED_ARG.value[0]
                            .format('values', '[<int>, [int], [int]]'))

        args = parser.parse_args()

        try:
            status = bulbs.change_color(ip=args.ip, values=tuple(args.color_values), color_mode=args.color_mode)
            return handler.return_success(status=status)
        except Exception as e:
            logging.exception(APIStatusMessage.ERROR.value[0])
            handler.return_exception(
                status=APIStatusMessage.ERROR,
                params=args,
                traceback=traceback.format_exc(),
                exception=e
            )

    @staticmethod
    def get():
        """
        get bulb current color by ip
        :return:
        """
        return handler.return_exception(
            status=APIStatusMessage.METHOD_NOT_DEFINED,
            params=None
        )
