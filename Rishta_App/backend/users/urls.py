from django.urls import re_path
from rest_framework.routers import DefaultRouter

from backend.users.views.activate_account import activate
from backend.users.views.users import UserAPIViewSet

APP_BASE_URL = r'users'

router = DefaultRouter()
router.register(APP_BASE_URL, UserAPIViewSet, basename='user')

urlpatterns = router.urls + [
    re_path(
        APP_BASE_URL + r'/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]+-[0-9A-Za-z]+)/activate/?',
        activate,
        name='activate'
    ),
]
