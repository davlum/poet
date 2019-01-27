from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _
from app import views

# https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#translating-url-patterns
urlpatterns = [
    path('', views.index, name='index'),
    path(_('home'), views.home, name='home'),
    path(_('work/<int:work_id>'), views.work, name='work'),
    path(_('collection/<int:collection_id>'), views.collection, name='collection'),
    path(_('entity/<int:entity_id>'), views.entity, name='entity'),
    path(_('search/'), views.search, name='search'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
