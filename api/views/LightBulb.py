import logging
import traceback
from flask_restful import Resource, reqparse
from api.models.ResponseHandler import ResponseHandler as Handler, APIStatus, APIMessage
from api.models.BulbController import BulbController as Bulbs
from api.views.Authentication import auth


class LightBulb(Resource):
    decorators = [auth.login_required]

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
            response = Bulbs.get_bulbs(ip=args.ip, metadata=True)

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
            return Handler.success(response={args.property: response})
        except Exception as e:
            logging.exception(return_status.value.get('message'))
            return Handler.exception(
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
            status = Bulbs.rename_bulb(ip=args.ip, new_name=args.new_name)
            return Handler.success(response=status)
        except Exception as e:
            logging.exception(APIStatus.ERROR.value.get('message'))
            return Handler.exception(
                status=return_status,
                exception=e,
                traceback=traceback.format_exc(),
                params=args
            )
