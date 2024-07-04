# your_app_name/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/test/(?P<attempt_id>[0-9a-f-]+)/$', consumers.TestConsumer.as_asgi()),
]