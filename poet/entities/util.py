from django.db import connection
from django.http import Http404
from typing import List, Dict
from pojo.settings import STATIC_URL
import pathlib
import os


def enrich_work(work_dict: Dict[str, str]) -> Dict[str, str]:
    return {
        'name': get_dashed_name(work_dict),
        'codec': get_codec(work_dict),
        'full_path': get_full_path(work_dict),
        **work_dict
    }


def get_string_location(model_dict):
    name_ls = [model_dict['city'], model_dict['country']]
    return ' - '.join([x for x in name_ls if x is not None])


def get_codec(dict_or_work):
    if dict_or_work['path_to_file'] is None:
        return None
    return 'audio/{}'.format(pathlib.PurePosixPath(dict_or_work['path_to_file']).suffix.replace('.', ''))


def get_full_path(dict_or_work):
    if dict_or_work['path_to_file'] is None:
        return None
    return os.path.join(STATIC_URL, dict_or_work['file_type'], dict_or_work['path_to_file'])


class Context:

    def __init__(self, template, data):
        self.template = template
        self.data = data

    template: str
    data: Dict


def raise_(e):
    raise e


def to_none(s):
    """Converts identity objects to None"""
    if s is None:
        return s
    if type(s) is dict and not s:
        return None
    if type(s) is list and not s:
        return None
    if type(s) is str and not s.strip():
        return None
    return s


def get_or_404(query_result, message=None):
    try:
        return query_result[0]
    except IndexError:
        if message is not None:
            raise Http404(message)
        else:
            raise Http404()


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


def get_dashed_name(model_dict: Dict[str, str]) -> str:
    return get_dashed_list(['full_name', 'alt_name'], model_dict)


def get_dashed_date(model_dict: Dict[str, str]) -> str:
    return get_dashed_list(['start_date', 'end_date'], model_dict)


def get_dashed_list(key_ls, d) -> str:
    str_ls = [d[k] for k in key_ls]
    return ' - '.join([x for x in str_ls if x is not None])