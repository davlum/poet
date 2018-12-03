from django.db import connection
from django.http import Http404
from typing import List, Dict
from poet.models.entity import Entity


class Context:

    def __init__(self, template, data):
        self.template = template
        self.data = data

    template: str
    data: Dict


def raise_(e):
    raise e


def get_or_404(query_result, message=None):
    try:
        return query_result[0]
    except IndexError:
        if message is not None:
            raise Http404(message)
        else:
            raise Http404()


def get_entity_name(entity_id):
    entity = Entity.objects.get(pk=entity_id)
    names_ls = [entity.full_name, entity.alt_name]
    names_ls = ' - '.join([x for x in names_ls if x is not None])
    return names_ls


def to_dict(cursor):
    """
    Return all rows from a cursor as a dict
    :param cursor:
    :return:
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def query(query_string: str, query_args: List) -> List[Dict]:
    with connection.cursor() as cursor:
        cursor.execute(query_string, query_args)
        return to_dict(cursor)


def query_one(query_string: str, query_args: List, message=None):
    return get_or_404(query(query_string, query_args), message)