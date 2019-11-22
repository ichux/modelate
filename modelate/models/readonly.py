from flask import _request_ctx_stack as context_stack
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import sessionmaker, scoped_session

from modelate import app, db

READONLY_SESSION = scoped_session(sessionmaker(bind=db.get_engine(app, bind='readonly')),
                                  scopefunc=context_stack.__ident_func__)


# activate in case there are issues
# @app.teardown_request
# def teardown_request(exception=None):
#     if not app.testing:
#         READONLY_SESSION.remove()


class ReadOnly(object):
    def __init__(self):
        pass

    @staticmethod
    def session():
        # from sqlalchemy import create_engine
        # db_uri = app.config["SQLALCHEMY_BINDS"]["readonly"]

        """
        _setdefault('pool_size', 'SQLALCHEMY_POOL_SIZE')
        _setdefault('pool_timeout', 'SQLALCHEMY_POOL_TIMEOUT')
        _setdefault('pool_recycle', 'SQLALCHEMY_POOL_RECYCLE')
        _setdefault('max_overflow', 'SQLALCHEMY_MAX_OVERFLOW')
        """
        # http://docs.sqlalchemy.org/en/latest/core/pooling.html
        # http://derrickgilland.com/posts/demystifying-flask-sqlalchemy/
        # http://stackoverflow.com/questions/29224472/sqlalchemy-connection-pool-and-sessions
        # engine = create_engine(db_uri)

        # from werkzeug.local import LocalProxy
        # session = scoped_session(sessionmaker(bind=ENGINE))
        # return LocalProxy(lambda: session)
        return READONLY_SESSION

    @staticmethod
    def base_class(query):
        """
        A hack to get the paginate to work for the default "sqlalchemy.orm.query.Query"

        For a long time running application, assigning the __class__ attribute is useful:
        1. you need to replace an old version of an object by a newer version of the same class without loss of data
        e.g. after some reload(module) and without reload of unchanged modules.
        2 if you implement persistency - something similar to pickle.load.

        I can't write the complete code before starting the application.

        :param query:
        :return:
        """
        query.__class__ = BaseQuery
        return query
