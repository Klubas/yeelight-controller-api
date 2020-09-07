import logging
import traceback
from flask_restful import Resource, reqparse
from api.models.ResponseHandler import ResponseHandler as Handler, APIStatus, APIMessage
from api.models.BulbController import bulbs
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
            return Handler.success(response=status)
        except Exception as e:
            logging.exception(APIStatus.ERROR.value.get('message'))
            return Handler.exception(
                status=APIStatus.ERROR,
                params=args,
                traceback=traceback.format_exc(),
                exception=e
            )
