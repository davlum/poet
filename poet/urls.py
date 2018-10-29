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
    path('work/<int:work_id>', views.work, name='work'),
    path('search/', views.search, name='search'),
    path('search/<entity:entity_name>', views.search, name='search')
]