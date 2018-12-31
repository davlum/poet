from jinja2 import Environment
from django.contrib import messages
from app.controllers.search import get_search_fields
from django.contrib.staticfiles.storage import staticfiles_storage


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'get_messages': messages.get_messages,
        'get_search_fields': get_search_fields
        })
    return env
