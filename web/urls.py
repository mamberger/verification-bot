from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from telegram_api.views import show_ftp

from users import views

urlpatterns = [
    path('', views.LoginView.as_view(), name="login_page"),
    path('login', views.LoginView.as_view(), name="mirror_login_page"),
    path('api/', include('api.urls')),
    path('user/', include("users.urls")),
    path('accounts/', include("accounts.urls")),
    
    path('form/user/', include("users.form_urls")),
    path('telegram/', show_ftp, name="show_telegram_photos"),

    path('drop/', include("drop.urls")),

    path('admin/', admin.site.urls),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns+=staticfiles_urlpatterns()
