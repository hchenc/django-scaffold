from django.conf.urls import (url, include)

from efunds.urls import urlpatterns

urlpatterns = [
    url('^asd/', include(urlpatterns))
]