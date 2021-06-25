from django.urls import path, include
from . import views

app_name = 'user'

urlpatterns = [
    path('', include('djoser.urls')),
    path('users/reviews/', views.UserReviews.as_view(), name='User Review'),
    path('jwt/create/', views.VirtueleTokenObtainPairView.as_view()),
    path('jwt/refresh/', views.VirtueleTokenRefreshView.as_view()),
]