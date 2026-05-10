from rest_framework import status
from rest_framework.response import Response

from common.constants.messages import ApiMessage


def success_response(data=None, message=ApiMessage.SUCCESS, status_code=status.HTTP_200_OK):
    return Response(
        {
            "success": True,
            "message": message,
            "data": data,
        },
        status=status_code,
    )


def error_response(errors=None, message=ApiMessage.SERVER_ERROR, status_code=status.HTTP_400_BAD_REQUEST):
    return Response(
        {
            "success": False,
            "message": message,
            "errors": errors,
        },
        status=status_code,
    )
