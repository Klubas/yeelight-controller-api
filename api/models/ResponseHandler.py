import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

tb = True if os.getenv('YC_DEBUG') == 'True' else False


class APIMessage(Enum):
    VALUE_ERROR_ARG = \
        {"message": "Value '{}' for '{}' is invalid", "code": 400}

    REQUIRED_ARG = \
        {"message": "Argument '{}' must be specified. Details: [{}]", "code": 400}


class APIStatus(Enum):
    ID_REQUIRED = \
        {"message": "Param ID is required for this action.", "code": 400}

    IP_REQUIRED = \
        {"message": "Param IP is required for this action.", "code": 400}

    IP_INVALID = \
        {"message": "Supplied IP is invalid.", "code": 400}

    BULB_NOT_FOUND = \
        {"message": "Bulb not found.", "code": 400}

    VALUE_ERROR = \
        {"message": "Supplied value is invalid:", "code": 400}

    SUCCESS = \
        {"message": "Operation performed successfully", "code": 200}

    LOGIN_SUCCESS = \
        {"message": "Login successful", "code": 200}

    LOGIN_ERROR = \
        {"message": "Invalid credentials.", "code": 401}

    ERROR = \
        {"message": "Internal server error.", "code": 500}

    METHOD_NOT_DEFINED = \
        {"message": "Not defined", "code": 501}


class ResponseHandler:
    @staticmethod
    def exception(status, params, exception=None, traceback=None, **kwargs):
        """
        Used for returning exception messages via API
        :return:
        """

        description = status.value.get('message')

        response = {
            'message': {
                "status": status.name,
                "description": description
            }
        }

        if exception:
            response['message']['response'] = str(exception)

        if params:
            response['message']['params'] = params

        if traceback and tb:
            response['message']['traceback'] = str(traceback)

        return_code = status.value.get('code')
        return response, return_code

    @staticmethod
    def success(response, status=APIStatus.SUCCESS, **kwargs) -> dict and int:
        """
        Retorno de sucesso
        :return:
        """

        description = status.value.get('message')

        response = {
            'message': {
                "status": status.name,
                "description": description,
                'response': response
            }
        }
        return_code = status.value.get('code')
        return response, return_code



