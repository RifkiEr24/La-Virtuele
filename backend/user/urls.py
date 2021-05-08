from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'user'

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    # path('jwt/create/custom/', views.CustomTokenObtainPairView.as_view()),
    # path('jwt/refresh/custom/', views.CustomTokenRefreshView.as_view()),
]