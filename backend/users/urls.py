from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet

app_name = 'users'

router = DefaultRouter()

router.register('users', CustomUserViewSet)

users_patterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
]

urlpatterns = [
    path('', include(users_patterns)),
    path('auth/', include('djoser.urls.authtoken')),
]
