

from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
   openapi.Info(
      title="Stackoverflow clone",
      default_version='v1',
      description="Backend clone of stackoverflow website.",
   ),
   public=True,
   permission_classes=[AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include('users.urls')),
    path("posts/", include('posts.urls')),

    path('login/token/', csrf_exempt(TokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('login/token/refresh/', csrf_exempt(TokenRefreshView.as_view()), name='token_refresh'),

    path('', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc'), name='schema-redoc'),
]
