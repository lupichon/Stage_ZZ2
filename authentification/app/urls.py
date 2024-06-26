from django.urls import path
from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",views.home,name = "home"),
    path("register",views.register,name = "register"),
    path("login",views.lOgin, name = "login"),
    path("logout", views.logOut, name = "logout"),
    path("activate/<uidb64>/<token>",views.activate,name="activate"),

    path("reset_password", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("reset_password_send", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset_password_complete", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]