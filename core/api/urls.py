from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from .views import UserViewSet, RestaurantViewSet, FavoritiesViewSet, ReserveViewSet, CommentViewSet, MyTokenObtainPairView, ForgetApiView, ResetApiView, ActivateUserApi

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenBlacklistView

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'restaurant', RestaurantViewSet)
router.register(r'favoritie', FavoritiesViewSet)
router.register(r'reserve', ReserveViewSet)
router.register(r'comment', CommentViewSet)

router.register(r'device', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('forget/', csrf_exempt(ForgetApiView.as_view()), name = 'forget'),
    path('reset/<uidb64>/<token>', ResetApiView.as_view(), name='reset_password'),
    path('activate/<uidb64>/<token>', ActivateUserApi.as_view(), name='activate_user'),
    path('', include(router.urls))
]