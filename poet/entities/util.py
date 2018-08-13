from django.db import connection
from django.http import Http404
from typing import List


def get_or_404(query_result, message=None):
    try:
        return query_result[0]
    except IndexError:
        if message is not None:
            raise Http404(message)
        else:
            raise Http404()


def dictfetchall(cursor):
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


def query(query_string: str, query_args: List):
    with connection.cursor() as cursor:
        cursor.execute(query_string, query_args)
        return dictfetchall(cursor)


def query_one(query_string: str, query_args: List, message=None):
    return get_or_404(query(query_string, query_args), message)