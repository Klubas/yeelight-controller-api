from enum import Enum

tb = True


class APIStatusMessage(Enum):
    IP_REQUIRED = "Param IP is required for this action.", 400
    IP_INVALID = "Supplied IP is invalid.", 400
    REQUIRED_ARG = "Argument '{}' must be specified. Details: [{}]", 400
    SUCCESS = "Operation performed successfully", 200
    ERROR = "Internal server error.", 500
    METHOD_NOT_DEFINED = "Not defined", 501


class ResponseHandler:
    @staticmethod
    def return_exception(status, params, exception=None, traceback=None):
        """
        Used for returning exception messages via API
        :return:
        """
        response = {
            'message': {
                "status": status.value[0]
            }
        }

        if exception:
            response['message']['response'] = str(exception)

        if traceback and tb:
            response['message']['traceback'] = str(traceback)

        if params:
            response['message']['params'] = params

        return_code = status.value[1]
        return response, return_code

    @staticmethod
    def return_success(status, message=APIStatusMessage.SUCCESS) -> dict and int:
        """
        Retorno de sucesso
        :return:
        """
        status = {
            'message': {
                "status": message.value[0],
                'response': status
            }
        }
        return_code = message.value[1]
        return status, return_code
