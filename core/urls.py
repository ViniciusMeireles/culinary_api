from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

django_urlpatterns = [
    path("admin/", admin.site.urls),
]

third_party_urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

local_urlpatterns = [
    path("", RedirectView.as_view(pattern_name='swagger-ui'), name='home'),
    path("users/", include("user.urls")),
    path("recipes/", include("recipe.urls")),
]

urlpatterns = (
    django_urlpatterns
    + third_party_urlpatterns
    + local_urlpatterns
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
