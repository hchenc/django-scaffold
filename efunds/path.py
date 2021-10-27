from django.conf.urls import (url, include)

from efunds.urls import urlpatterns
from django.conf import settings

app_name = getattr(settings, 'APP_NAME', '')

if app_name:
    urlpatterns = [
        url('^{}/'.format(app_name), include(urlpatterns))
    ]
else:
    urlpatterns = urlpatterns

