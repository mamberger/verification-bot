from django.urls import path
from django.views.generic import TemplateView
from .views import RequestChecking, CardChecking, RequestCreate, RequestStatusChange,ReferalsChecking, ReferalCreate,PhotoUpdate


urlpatterns = [
    path('request_check', RequestChecking.as_view()),
    path('request_create', RequestCreate.as_view()),
    path('request_edit', RequestStatusChange.as_view()),
    path('card_check', CardChecking.as_view()),
    path('referals_check', ReferalsChecking.as_view()),
    path('referals_create', ReferalCreate.as_view()),
    path('photo_update', PhotoUpdate.as_view()),
]