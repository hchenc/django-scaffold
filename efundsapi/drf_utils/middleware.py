import uuid

from libs import logger


class RequestIdMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return response

    def process_request(self, request):
        setattr(request, 'id', uuid.uuid4().hex)


class RequestLogMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return response

    def process_request(self, request):
        log = logger.get_thread_logger()
        setattr(request, 'log', log)
        log.bind(request_id=request.id)
        log.info('Get a request: ',
                 params=request.GET.dict(),
                 body=request.body.decode("utf-8") or {})
