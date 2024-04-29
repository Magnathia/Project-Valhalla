from django.urls import path
from .views import user_login, UserRegisterView, user_logout, user_profile, UserPasswordChangeView, UserPasswordResetView, UserPasswordResetConfirmView, dashboard

urlpatterns = [
    # Authentication URLs
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),  # Use the custom logout view
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', UserPasswordChangeView.as_view(), name='password_change_done'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', UserPasswordResetView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', UserPasswordResetConfirmView.as_view(), name='password_reset_complete'),
    path('dashboard/', dashboard, name='dashboard'),

    # User profile and registration URLs
    path('profile/', user_profile, name='profile'),
    path('register/', UserRegisterView.as_view(), name='register'),
]

