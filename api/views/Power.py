import logging
import traceback
from flask_restful import Resource, reqparse
from api.models.ResponseHandler import ResponseHandler as Handler, APIStatus, APIMessage
from api.models.BulbController import bulbs
from api.views.Authentication import auth


class Power(Resource):
    decorators = [auth.login_required]

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
            return Handler.success(response=status)
        except Exception as e:
            logging.exception(APIStatus.ERROR.value.get('message'))
            return Handler.exception(
                status=APIStatus.ERROR,
                params=args,
                traceback=traceback.format_exc(),
                exception=e)