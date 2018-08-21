# http://flask.pocoo.org/docs/patterns/packages/
from functools import wraps

from flask import request

from modelate import app
from modelate.exceptions import InvalidLength


def contexts(*args):
    context = {
        'path': request.path,
        'base_url': request.url_root,
        'method': request.method,
        'headers': dict(request.headers),
    }
    if '?' in request.url:
        context['query_string'] = request.url[(request.url.find('?') + 1):]

    return [context] + list(args)


def get_size(the_file):
    if the_file.content_length:
        return the_file.content_length

    try:
        pos = the_file.tell()
        the_file.seek(0, 2)  # seek to end
        size = the_file.tell()
        the_file.seek(pos)  # back to original position
        return size
    except (AttributeError, IOError):
        pass

    # in-memory file object that doesn't support seeking or tell
    return 0  # assume small enough


def limit_length(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        filed = request.files['file']
        content_length = get_size(filed)  # or request.content_length
        max_length = app.config['MAX_FILE_SIZE']

        if content_length > max_length:
            raise InvalidLength(f'Maximum file size allowed: {max_length}kB. Size of file sent in {content_length}')
        if content_length == 0:
            raise InvalidLength('0kB file detected')

        return f(*args, **kwargs)

    return wrapper
