from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from app import views


# https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#translating-url-patterns
# We ultimately decided to leave links in just one language, The problem with translated URLs
# was raised in this issue;
# https://github.com/davlum/poet/issues/30
urlpatterns = [
    path('', views.index, name='index'),
    path('inicio', views.home, name='home'),
    path('obra/<int:work_id>', views.work, name='work'),
    path('serie/<int:collection_id>', views.collection, name='collection'),
    path('entidad/<int:entity_id>', views.entity, name='entity'),
    path('buscar/', views.search, name='search'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
