from django.urls import path, include
from django.contrib.auth import views as auth_views
from user.views import UserUpdate, UserDetailsView, EmailUpdate, AvatarUpdate, BackgroundUpdate, ChangePasswordDoneView

urlpatterns = [
    path('<int:pk>/', UserDetailsView.as_view(), name='profile'),
    path('<int:pk>/edycja', UserUpdate.as_view(), name='profile-edit'),
    path('<int:pk>/edycja/email', EmailUpdate.as_view(), name='email-edit'),
    path('<int:pk>/edycja/haslo',
         auth_views.PasswordChangeView.as_view(template_name='users/password_update.html'),
         name='password-edit'),
    path('update/password/success/', ChangePasswordDoneView.as_view(),
         name='password_change_done'),
    path('<int:pk>/edycja/avatar', AvatarUpdate.as_view(), name='avatar-edit'),
    path('<int:pk>/edycja/background', BackgroundUpdate.as_view(), name='background-edit'),
]
