import logging
import traceback
from flask_restful import Resource, reqparse
from api.models.BulbController import BulbController as Bulbs
from api.views.Authentication import auth
from api.models.ResponseHandler import ResponseHandler as Handler, APIStatus


class LightBulbs(Resource):
    decorators = [auth.login_required]

    @staticmethod
    def get():
        """
        Get list of bulbs metadata (ip, name, model, power state, color)
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('fake_bulbs', type=int, required=False, default=0,
                            help='Generate n fake bulbs for testing purposes')
        args = parser.parse_args()

        try:
            response = Bulbs.get_bulbs()

            if len(response) > 0:
                fake_response = []
                for index in range(0, len(response)):
                    fake_response.append(response[index].copy())
                for index in range(len(response), len(response) + args.fake_bulbs):
                    fake_response.append(response[0].copy())
                for index in range(len(response), len(fake_response)):
                    fake_response[index]["id"] = "fake_" + str(index)
                response = fake_response

            return Handler.success(response=response)

        except Exception as e:
            return Handler.exception(
                status=APIStatus.ERROR,
                exception=e,
                traceback=traceback.format_exc(),
                params=None
            )
