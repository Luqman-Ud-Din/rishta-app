from django.urls import path
from rest_framework.routers import DefaultRouter

from backend.users.views.activate_account import activate
from backend.users.views.users import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
urlpatterns = router.urls + [
    path(
        r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/?',
        activate,
        name='activate'
    ),
]
