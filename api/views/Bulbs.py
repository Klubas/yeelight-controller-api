import logging
import traceback
from flask_restful import Resource
from api.models.BulbController import BulbController as bulbs
from api.views.Authentication import auth
from api.models.ResponseHandler import ResponseHandler as Handler, APIStatus


class Bulbs(Resource):
    decorators = [auth.login_required]

    @staticmethod
    def get():
        """
        Get list of bulbs metadata (ip, name, model, power state, color)
        :return:
        """
        try:
            response = bulbs.get_bulbs(metadata=True)
            return Handler.success(response=response)
        except Exception as e:
            logging.exception(APIStatus.ERROR.value.get('message'))
            return Handler.exception(
                status=APIStatus.ERROR,
                exception=e,
                traceback=traceback.format_exc(),
                params=None
            )