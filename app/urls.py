from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('work/<int:work_id>', views.work, name='work'),
    path('collection/<int:collection_id>', views.collection, name='collection'),
    path('entity/<int:entity_id>', views.entity, name='entity'),
    path('search/', views.search, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
