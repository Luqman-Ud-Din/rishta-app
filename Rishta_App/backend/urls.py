"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from backend.swagger.urls import urlpatterns as swagger_urls
from backend.users.urls import urlpatterns as user_urls
from backend.events.urls import urlpatterns as event_urls
from backend.users.views.otp import CustomeTokenObtainPairView

# urlpatterns = [
#     # ...
#     # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
#     #   * `title` and `description` parameters are passed to `SchemaGenerator`.
#     #   * Provide view name for use with `reverse()`.
#     path('openapi', get_schema_view(
#         title="Your Project",
#         description="API for all things …"
#     ), name='openapi-schema'),
#     # ...
# ]

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('admin/', admin.site.urls),
    path('swagger/', include(swagger_urls)),
    path('tinymce/', include('tinymce.urls')),
    path('api/token/', CustomeTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(user_urls)),
    path('api/', include(event_urls))
]
