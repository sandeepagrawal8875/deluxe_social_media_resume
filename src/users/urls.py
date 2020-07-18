from django.urls import path
from users import views as users_views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', users_views.home, name='home1'),
    path('register', users_views.register, name='register'),
    path('login/', users_views.login_page, name='login'),
    path('logout/', users_views.logout_User, name='logout'),

    path('create/profile/', users_views.profile , name='profile_create'),


    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),name="reset_password"),

    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_sent.html"),name="password_reset_done"),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_form.html"),name="password_reset_confirm"),

    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_done.html"),name="password_reset_complete"),

]
