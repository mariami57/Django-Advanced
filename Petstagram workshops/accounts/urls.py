from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from accounts import views
from accounts.views import RegisterView, ProfileEditView, ProfileDetailsView

urlpatterns = [

    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="accounts/login-page.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", include([
        path("",ProfileDetailsView.as_view(), name="profile-details"),
        path("edit/", ProfileEditView.as_view(), name="profile-edit"),
        path("delete/", views.app_user_delete_view, name="profile-delete"),

    ])),

]