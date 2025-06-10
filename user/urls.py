from django.urls import path
from .views import RegisterView, UserProfileView, UpdateUserProfileView, ChangePasswordView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
   path('register/', RegisterView.as_view()),
   path('profile/', UserProfileView.as_view(), name='user-profile'),
   path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('profile/update/', UpdateUserProfileView.as_view(), name='user-profile-update'),
   path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
