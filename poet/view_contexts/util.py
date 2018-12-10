from django.db import connection
from django.http import Http404
from typing import List, Dict
import pathlib
from pydub import AudioSegment
import math


def return_or_404(f, message=None, **kwargs):
    try:
        return f(**kwargs)
    except IndexError:
        if message is not None:
            raise Http404(message)
        else:
            raise Http404


def normalize(arr):
    max_val = abs(max(arr, key=abs))
    min_val = abs(min(arr, key=abs))
    denom = max_val - min_val
    return list(map(lambda x: round((x - min_val) / denom, 4), arr))


def get_peaks_from_audio_path(file, codec) -> List[float]:
    """

    :param file: Could be a string or file object
    :param codec: string of the codec of the file e.g. mp3, wav
    :return: a list of 1000 normalized samples from the audio file
    """
    audio = AudioSegment.from_file(file, codec)
    mono_audio = audio.set_channels(1)
    samples = mono_audio.get_array_of_samples()
    # We want to get about a thousand samples for drawing the waveform
    every_nth = math.floor(len(samples) / 1000)
    sliced_samples = samples[0::every_nth]
    return normalize(sliced_samples)


def get_extension(path: str) -> str:
    """
    :param path: returns the extension of the file without the .
    :return: file extension e.g. jpg, wav
    """
    return pathlib.PurePosixPath(path).suffix.replace('.', '')


class Context:

    def __init__(self, template, data):
        self.template = template
        self.data = data

    template: str
    data: Dict


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


def get_dashed_location(model_dict):
    return get_dashed_list(['city', 'country'], model_dict)


def get_dashed_name(model_dict: Dict[str, str]) -> str:
    return get_dashed_list(['full_name', 'alt_name'], model_dict)


def get_dashed_date(model_dict: Dict[str, str]) -> str:
    return get_dashed_list(['start_date', 'end_date'], model_dict)


def get_dashed_list(key_ls, d) -> str:
    str_ls = [d[k] for k in key_ls]
    return ' - '.join([x for x in str_ls if x is not None])