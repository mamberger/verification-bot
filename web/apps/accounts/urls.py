from django.urls import path
from .views import all_view, detail_view, delete_view, take_view, setbalance_view, ban_add_view, change_status_view, \
    delete_account, new_all_view

urlpatterns = [
    path('view/delete__account/<int:account_id>', delete_account),
    path('change__status/<int:account_id>/<str:status>/<int:detail>', change_status_view, name='change_status'),
    path("<str:show_type>/", new_all_view, name="view_all_accounts"),
    #path("<str:show_type>/", all_view, name="view_all_accounts"),
    path("view/<int:account_id>", detail_view, name="detail_accounts_view"),
    path("delete/<int:account_id>", delete_view, name="delete_account"),
    path("take/<int:account_id>", take_view, name="take_account"),
    path("setbalance/<account_id>", setbalance_view, name="setbalance_view"),
    path("banlist/add/<int:account_id>", ban_add_view, name="ban_add_view"),
]
