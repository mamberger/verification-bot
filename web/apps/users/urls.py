from django.urls import path
from .form_view import flogin_view, logout_view
from .views import CabinetView, ListView, AddView, delete_user

app_name = "users"

urlpatterns = [
    path("", CabinetView.as_view(), name="cabinet_view"),
    path("list", ListView.as_view(), name="list_users_view"),
    path("add", AddView.as_view(), name="add_user_view"),
    path("delete/<int:user_id>", delete_user, name="delete_user_view"),

    path("logout", logout_view, name="cabinet_logout")
]
