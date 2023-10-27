from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from . import views
urlpatterns = [
    path('',views.UserListView.as_view(),name='user_view'),
    path('signup/',views.UserView.as_view(),name='user_view'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:user_id>/',views.UserView.as_view(),name='Profile_view'),
    path('api/auth/logout/',TokenBlacklistView.as_view(),name='token_blacklist'),
    path('change_password/<int:pk>/', views.ChangePasswordView.as_view(), name='auth_change_password'),
    path('change_profile_image/',views.ChangeProfileImageView.as_view(),name='change_profile_image'),
]