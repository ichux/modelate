#!/usr/bin/env python

import math
import time

import datetime
import filecmp
import os
import secrets
import traceback
from flask import request
from flask_login import AnonymousUserMixin
from pprint import pprint
from sqlalchemy import MetaData
from urllib.parse import urlparse, parse_qs

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


def properties(flag):
    pprint([_ for _ in dir(flag) if not _.startswith('_')])


def parse_query(url):
    parsed_url = urlparse(url)
    # print(parsed_url)
    return parse_qs(parsed_url.query)


def to_curl(request_in):
    if urlparse(request_in.url).scheme.endswith('s'):
        command = "curl -k "
    else:
        command = "curl "

    headers = ["'{0}: {1}'".format(k, v) for k, v in request_in.headers.items()]
    headers = " -H ".join(sorted(headers))
    data = request_in.body or ""

    command += f"-X {request_in.method} -H {headers} "

    if data:
        command += f"-d '{data}' "

    return command + f"'{request_in.url}'"


# noinspection PyUnresolvedReferences
def to_unicode(value):
    """
    Forces a bytestring to become a Unicode string.
    """
    if isinstance(value, bytes):
        value = value.decode('utf-8', errors='replace')
    elif not isinstance(value, str):
        value = str(value)

    return value


# noinspection PyUnresolvedReferences
def to_bytes(value):
    """
    Forces a Unicode string to become a bytestring.
    """
    if isinstance(value, str):
        value = value.encode('utf-8', 'backslashreplace')

    return value


# metadata = MetaData(naming_convention=convention, schema='public')  # public as in the case of Postgres
metadata = MetaData(naming_convention=convention, schema=None)


def extract_post_values(form):
    return dict((key, form.getlist(key) if len(form.getlist(key)) > 1 else form.getlist(key)[0]) for key in form.keys())


def is_json():
    return (request.mimetype == 'application/json' or request.is_xhr) and request.accept_mimetypes.accept_json


def extract_vars(form):
    # vars = extract_vars(request.form)
    response = {}
    for key, value in form.items():
        if isinstance(value, list) and len(value) == 1:
            value = value[0]
        if key not in response:
            response[key] = value
        elif isinstance(response[key], list):
            response[key].append(value)
        else:
            response[key] = [response[key], value]
    return response


def prepare_arguments(request_args):
    """Prepare DataTables with default arguments.
    :param request_args: request.args are supplied by flask
    :type request_args: flask dictionary data type
    """
    request_values = dict()
    for key, value in request_args.items():
        try:
            request_values[key] = int(value)
        except ValueError:
            if value in ('true', 'false'):
                request_values[key] = value == 'true'
            else:  # assume string
                request_values[key] = value
    return request_values


def details(obj):
    """
    Does a pretty print of the object representation
    :param obj: the object to be pretty printed
    :return: a pretty print representation
    """
    pprint(vars(obj))


def get_real_ip():
    # use all known hack to get the real ip address of the visitor who caused the error
    address = request.headers.get('X-Forwarded-For')
    if address is not None:
        # An 'X-Forwarded-For' header includes a comma separated list of the
        # addresses, the first address being the actual remote address.
        ip = address.encode('utf-8').split(b',')[0].strip()
    else:
        # This is important for nginx config
        ip = request.environ.get('HTTP_X_REAL_IP')
        if ip is None:
            try:
                ip = request.access_route[0]
            except IndexError:
                ip = request.remote_addr
    return str(ip)


def strtobool(val):
    """Convert a string representation of truth to True or False.

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are anything else.
    """

    # the above was adapted from "from distutils.util import strtobool"
    if str(val).lower() in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    return False


def chunks(listed, n):
    """Yield successive n-sized chunks from listed."""
    for i in range(0, len(listed), n):
        yield listed[i:i + n]


def unique_id(nbytes=16):
    return secrets.token_hex(nbytes)


def get_exception_message(exception):
    message = ''

    if hasattr(exception, 'message'):
        if isinstance(exception.message, dict):
            message = exception.message.get('message')
        elif exception.message:
            message = exception.message

        return {"error": {'type': type(exception).__name__, "message": message}, "traceback": traceback.format_exc()}


# Custom Template Filters
def date_time_format(value):
    delta = datetime.datetime.now() - value
    if delta.days == 0:
        formatting = 'today'
    elif delta.days < 10:
        formatting = f'{delta.days} days ago'
    elif delta.days < 28:
        formatting = f'{int(math.ceil(delta.days / 7.0))} weeks ago'
    elif value.year == datetime.datetime.now().year:
        formatting = 'on %d %b'
    else:
        formatting = 'on %d %b %Y'
    return value.strftime(formatting)


def directory_size(path):
    total_size = 0
    seen = set()

    for dir_path, dir_names, file_names in os.walk(path):
        for fyl in file_names:
            file_path = os.path.join(dir_path, fyl)

            try:
                stat = os.stat(file_path)
            except OSError:
                continue

            if stat.st_ino in seen:
                continue

            seen.add(stat.st_ino)

            total_size += stat.st_size

    return get_size(total_size)


def get_size(size):
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    _int = int(math.floor(math.log(size, 1024)))
    s_ = round(size / math.pow(1024, _int), 2)

    return f'{s_}{size_name[_int]}' if s_ > 0 else '0B'


def file_details(infile):
    stat = os.stat(infile)

    # use the method below for an already opened file
    # fp = open("file.dat")
    # stat = os.fstat(fp.fileno())

    mtime = time.asctime(time.localtime(stat.st_mtime))
    atime = time.asctime(time.localtime(stat.st_atime))
    ctime = time.asctime(time.localtime(stat.st_ctime))

    return f"mtime: {mtime}, atime: {atime}, ctime: {ctime}"


def compare_files(first_file, second_file):
    """
    Does a byte-by-byte comparison
    :param first_file: the first input file
    :param second_file: the second input file
    :return: boolean
    """
    return filecmp.cmp(first_file, second_file, shallow=False)


# noinspection PyMethodMayBeStatic
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_admin(self):
        return False


def machine():
    _list = list(filter(None, [1, 3, 'a']))  # = [1, 3, 'a']
    _map = [x for x in map(int, ['1', '2', '3'])]  # = [1, 2, 3]

    dis = {'a': 1}
    dis.update({'b': 2, 'a': 3})  # == {'a': 3, 'b': 2}
    dis.setdefault('a', 4)  # 3
    # dis == {'a': 3, 'b': 2}

    return _list, _map


"""
# Caching
def cached(app, timeout=5 * 60, key='view/%s'):
    # http://flask.pocoo.org/docs/patterns/viewdecorators/#caching-decorator

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.path
            rv = app.cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            app.cache.set(cache_key, rv, timeout=timeout)
            return rv

        return decorated_function

    return decorator
"""
