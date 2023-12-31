

from django.urls import path

from profiles import views


urlpatterns = [
    path("login_view/", views.login_view, name="login_view"),
    path("logout_view/", views.logout_view, name="logout_view"),
    path("signup/", views.signup, name="signup"),
]
