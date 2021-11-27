import json
import logging
import traceback
from flask_restful import Resource, reqparse
from api.models.ResponseHandler import ResponseHandler as Handler, APIStatus, APIMessage
from api.models.BulbController import BulbController as Bulbs
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
        parser.add_argument('id', type=str, required=False,
                            help=APIStatus.ID_REQUIRED.value.get('message'))
        parser.add_argument('ip', type=str, required=False,
                            help=APIStatus.IP_REQUIRED.value.get('message'))
        parser.add_argument('state', type=str, required=False,
                            help=APIMessage.REQUIRED_ARG.value.get('message')
                            .format('state', 'on, off, toggle'))

        args = parser.parse_args()

        if not args.id and not args.ip:
            raise Exception("Bulb ID is required.")

        args.state = args.state if args.state else 'toggle'

        try:
            status = Bulbs.power(ip=args.ip, state=args.state, identifier=args.id)
            return Handler.success(response=status)
        except Exception as e:
            return Handler.exception(
                status=APIStatus.ERROR,
                params=args,
                traceback=traceback.format_exc(),
                exception=e
            )
