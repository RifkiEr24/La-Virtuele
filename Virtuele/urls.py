from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView
from product import urls as prod_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html"), name="app"),
    path('api/v1/', include([
        path('', include(prod_urls.urlpatterns), name="product")
    ]))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
