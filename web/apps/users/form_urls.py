from django.urls import  path
from .form_view import flogin_view, fadduser_view

urlpatterns = [
    path("login", flogin_view, name="form_view_login"),
    path("add", fadduser_view, name="form_view_add")
]
