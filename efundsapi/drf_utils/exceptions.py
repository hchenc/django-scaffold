from rest_framework import exceptions


class RequestExcpetion(exceptions.APIException):
    status_code = 500
    default_detail = 'request error to backends.'
    default_code = 'service_error'

    def __init__(self, detail=None, code=None, status_code=None):
        if status_code is not None:
            self.status_code = status_code
        super(RequestExcpetion, self).__init__(detail=detail, code=code)


class InvalidParameter(exceptions.APIException):
    status_code = 400
    default_detail = 'Some parameter is not valid.'
    default_code = 'bad_request'


class InvalidActionException(exceptions.APIException):
    status_code = 400
    default_detail = 'this action is not valid for the resource.'
    default_code = 'bad_request'


class ResourceNotFoundOrDeleted(exceptions.APIException):
    status_code = 404
    default_detail = 'Resource Not Found Or Deleted.'
    default_code = 'bad_request'


class ConflictStatus(exceptions.APIException):
    status_code = 409
    default_detail = 'Conflict Status'
    default_code = 'bad_request'


class ThresholdException(exceptions.APIException):
    status_code = 500
    default_detail = 'Not allowed to create now, may be up to limitation.'
    default_code = 'server_error'


class TeapotException(exceptions.APIException):
    status_code = 418
    default_detail = "I'm a teapot."
    default_code = "I'm a teapot"
