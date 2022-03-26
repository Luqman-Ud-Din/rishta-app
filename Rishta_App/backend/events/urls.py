from rest_framework.routers import DefaultRouter

from backend.events.views.events import EventsAPIViewSet


router = DefaultRouter()
router.register(r'', EventsAPIViewSet, basename='event')
urlpatterns = router.urls
