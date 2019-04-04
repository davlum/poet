from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import views as auth_views
from app import views


# https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#translating-url-patterns
urlpatterns = [
    path('', views.index, name='index'),
    path(_('home'), views.home, name='home'),
    path(_('work/<int:work_id>'), views.work, name='work'),
    path(_('collection/<int:collection_id>'), views.collection, name='collection'),
    path(_('entity/<int:entity_id>'), views.entity, name='entity'),
    path(_('search/'), views.search, name='search'),
    path(_('accounts/login/'), auth_views.LoginView.as_view(), name='login'),
    path(_('logout/'), auth_views.LogoutView.as_view(), name='logout'),
    path(_('password-reset/'), auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path(_('password-reset-done/'), auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(_('reset/<uidb64>/<token>/'), auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path(_('password-complete/'), auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
