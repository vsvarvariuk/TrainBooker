from django.urls import path

from user.views import UserCreateView, LoginView, ManageUserView

app_name = "user"

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="create-user"),

    path("login/", LoginView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="me")
]
