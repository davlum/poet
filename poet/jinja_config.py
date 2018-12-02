from jinja2 import Environment
from django.contrib import messages
import poet.templates.macros.py_jinja_functions as pyjfuns


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'get_messages': messages.get_messages,
        })
    env.globals['helpers'] = pyjfuns
    return env
