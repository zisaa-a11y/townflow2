from rest_framework import status
from rest_framework.views import exception_handler

from common.constants.messages import ApiMessage


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    details = response.data
    message = ApiMessage.SERVER_ERROR

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        message = ApiMessage.VALIDATION_ERROR
    elif response.status_code == status.HTTP_401_UNAUTHORIZED:
        message = ApiMessage.UNAUTHORIZED
    elif response.status_code == status.HTTP_403_FORBIDDEN:
        message = ApiMessage.FORBIDDEN
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        message = ApiMessage.NOT_FOUND

    response.data = {
        "success": False,
        "message": message,
        "errors": details,
    }
    return response
