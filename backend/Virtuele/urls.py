from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from product import urls as prod_urls
from user import urls as user_urls
from cart import urls as cart_urls
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title='Virtuele REST API',
      default_version='v1',
      description='REST API for La-Virtuele\'s Website',
      terms_of_service='https://www.google.com/policies/terms/',
      contact=openapi.Contact(email='virtuele.dev@gmail.com'),
      license=openapi.License(name='MIT License'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/', include([
        path('', include(prod_urls.urlpatterns), name='product'),
        path('', include(user_urls.urlpatterns), name='user'),
        path('', include(cart_urls.urlpatterns), name='cart'),
    ]), name='api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)