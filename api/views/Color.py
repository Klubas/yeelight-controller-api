import logging
import traceback
from flask_restful import Resource, reqparse
from api.models.ResponseHandler import ResponseHandler as Handler, APIStatus, APIMessage
from api.models.BulbController import BulbController as Bulbs
from api.views.Authentication import auth


class Color(Resource):
    decorators = [auth.login_required]

    @staticmethod
    def post():
        """
        Change bulb current color by ip
        :return:
        """
        parser = reqparse.RequestParser()

        parser.add_argument('ip', type=str, required=False,
                            help=APIStatus.IP_REQUIRED.value.get('message'))

        parser.add_argument('id', type=str, required=False,
                            help=APIStatus.ID_REQUIRED.value.get('message'))

        parser.add_argument('mode', dest='color_mode', type=str, required=True, location=['json', 'values'],
                            help=APIMessage.REQUIRED_ARG.value.get('message')
                            .format('mode', 'rgb, hsv, bright, temp'))

        parser.add_argument('values', dest='color_values', type=str, required=True, location=['json', 'values'],
                            help=APIMessage.REQUIRED_ARG.value.get('message')
                            .format('values', '[<int>, [int], [int]]'))

        args = parser.parse_args()

        if not args.id and not args.ip:
            raise Exception("Bulb ID is required.")

        color_values = args.color_values.split(',')
        color_values = list(map(int, color_values))

        try:
            status = Bulbs.change_color(
                ip=args.ip
                , values=tuple(color_values)
                , color_mode=args.color_mode
                , identifier=args.id
            )
            return Handler.success(response=status)
        except Exception as e:
            return Handler.exception(
                status=APIStatus.ERROR,
                params=args,
                traceback=traceback.format_exc(),
                exception=e
            )
