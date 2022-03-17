from django.urls import re_path
from rest_framework.routers import DefaultRouter

from backend.users.views.activate_account import activate
from backend.users.views.users import UserAPIViewSet

router = DefaultRouter()
router.register(r'', UserAPIViewSet, basename='user')

urlpatterns = router.urls + [
    re_path(
        r'activate',
        activate,
        name='activate'
    ),
]
