from django.urls import path, register_converter
from poet.entities.search import Entities
from . import views


class SearchParameterConverter:

    regex = '|'.join([entity.value for entity in Entities])

    def to_python(self, value):
        return Entities(value)

    def to_url(self, value):
        return str(value.value)


register_converter(SearchParameterConverter, 'entity')

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('autor/<int:artist_id>', views.artist, name='artist'),
    path('composicion/<int:composition_id>', views.composition, name='composition'),
    path('serie/<int:series_id>', views.series, name='series'),
    path('colectivo/<int:artist_id>', views.collective, name='collective'),
    path('search/', views.search, name='search'),
    path('search/<entity:entity_name>', views.search, name='search')
]