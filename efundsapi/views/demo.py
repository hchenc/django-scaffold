from efundsapi.drf_utils.response import APIResponse
from efundsapi.views import base
from efundsapi.models import Demo
from efundsapi.controller import demo
from efundsapi.serializers.serializers import DemoSerializer
from efundsapi.drf_utils.authentication import EfundsapiAuthentication


class DemoViewSet(base.EfundsAPIRetrieveModelMixin, base.EfundsAPIListModelMixin,
                  base.EfundsAPICreateModelMixin, base.EfundsAPIViewSet):
    authentication_classes = ()
    permission_classes = ()
    controller_class = demo.DemoController
    queryset = Demo.objects.all()
    serializer_class = DemoSerializer

    def list(self, request, *args, **kwargs):
        return APIResponse("ok")

    def retrieve(self, request, *args, **kwargs):
        params = request.query_params.dict()
        print(params)
        data = self.controller_class().get_object(123)

        return APIResponse(data)
