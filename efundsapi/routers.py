from rest_framework import routers
from efundsapi import views

v1 = routers.DefaultRouter(trailing_slash=False)

v1.register(r'demo', views.DemoViewSet, basename='demo')
