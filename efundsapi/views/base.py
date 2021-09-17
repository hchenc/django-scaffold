import logging

from rest_framework import viewsets, exceptions, filters, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from efundsapi.drf_utils.response import APIResponse
from efundsapi.drf_utils import exceptions as api_exceptions

LOG = logging.getLogger(__name__)


def pre_check_request(required_bodies=[], required_parameters=[]):
    def decorator(func):
        def wrapper(viewset, request, *args, **kwargs):
            qparams = request.query_params.dict()
            for key in required_parameters:
                if not qparams.get(key, None):
                    message = '%s is not provided in query params.' % key
                    raise api_exceptions.InvalidParameter(message)
            for key in required_bodies:
                if not request.data.get(key, None):
                    message = '%s is not provided in body.' % key
                    raise api_exceptions.InvalidParameter(message)
            return func(viewset, request, *args, **kwargs)

        return wrapper

    return decorator


class EfundsAPIViewSet(viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_fields = []
    valid_actions = []
    lookup_field = 'id'


class EfundsAPIListModelMixin(mixins.ListModelMixin, EfundsAPIViewSet):
    def list(self, request, *args, **kwargs):
        res = super(EfundsAPIListModelMixin, self).list(request, args, kwargs)
        extra = {
            'count': res.data['count'],
            'next': res.data['next'],
            'previous': res.data['previous']
        }
        return APIResponse(data=res.data['results'], extra=extra)


class EfundsAPICreateModelMixin(mixins.CreateModelMixin, EfundsAPIViewSet):
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.controller_class().create(**data)
        LOG.info('%s is created by %s.' % (obj.uuid, request.user.username))
        serializer = self.get_serializer(obj)
        return APIResponse(data=serializer.data)


class EfundsAPIRetrieveModelMixin(mixins.RetrieveModelMixin, EfundsAPIViewSet):
    def retrieve(self, request, *args, **kwargs):
        res = super(EfundsAPIRetrieveModelMixin, self).retrieve(
            request, args, kwargs)
        return APIResponse(res.data)


class EfundsAPIDestroyModelMixin(mixins.DestroyModelMixin, EfundsAPIViewSet):
    def destroy(self, request, *args, **kwargs):
        ins = self.get_object()
        self.controller_class().delete(ins.id)
        LOG.info('%s is deleted by %s.' % (ins.id, request.user.username))
        return APIResponse({}, status=204)

