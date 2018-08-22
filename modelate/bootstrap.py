import logging
import os
import sys
from functools import wraps

log = logging.getLogger(__name__)


def catch_error(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except AssertionError as exc:
            log.error(f'Error: {exc}')
            sys.exit(1)

    return wrapped


@catch_error
def primer():
    """
    Ensure that the start up environment has all the necessary variables.
    :return: None
    """
    assert os.getenv('SECRET_KEY'), "SECRET_KEY is missing"
    assert os.getenv('MODELATE_STATUS'), "MODELATE_STATUS is missing: `development`, `live` or `test` (default)"

    # Postgres section
    assert os.getenv('POSTGRES_DB'), "POSTGRES_DB is missing"
    assert os.getenv('POSTGRES_HOST'), "POSTGRES_HOST is missing"
    assert os.getenv('POSTGRES_PORT'), "POSTGRES_PORT is missing"
    assert os.getenv('POSTGRES_PASSWORD'), "POSTGRES_PASSWORD is missing"
    assert os.getenv('POSTGRES_USERNAME'), "POSTGRES_USERNAME is missing"

    # DB type
    assert os.getenv('DB_TYPE'), "DB_TYPE is missing"


primer()
