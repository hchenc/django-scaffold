from django.conf.urls import url, include

from efundsapi import routers
from efundsapi.views.version import get_version

urlpatterns = [
    url(r'^v1/', include(routers.v1.urls)),
    url(r'^$', get_version)
]
