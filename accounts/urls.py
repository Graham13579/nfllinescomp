from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views

app_name='accounts'

urlpatterns=[
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('passwordreset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form_ndf.html'),name='passwordreset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done_ndf.html'),name='passwordresetdone'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm_ndf.html'),name='passwordresetconfirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete_ndf.html'),name='passwordresetcomplete')
]