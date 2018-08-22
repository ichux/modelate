from collections import OrderedDict
from datetime import datetime
from json import dumps, loads
from pprint import pprint

# noinspection PyUnresolvedReferences
from psycopg2.extensions import adapt as sqlescape
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.attributes import InstrumentedAttribute

from modelate import db, app
from modelate.helpers import get_exception_message
from modelate.models.readonly import ReadOnly

from modelate.models.db_extra import Evolve

# FOR THE DB
CASCADE = app.config.get("CASCADE")
LAZY = app.config.get("LAZY")
ROS = ReadOnly.session()
ROS_BASE_CLASS = ReadOnly.base_class


class QueryPostgres(object):
    def __init__(self):
        pass

    @staticmethod
    def get_postgres_tables(namespace):
        sql = ("SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace "
               f"WHERE n.nspname = {namespace} AND c.relkind = 'r'")

        with db.engine.connect() as connection:
            tables = [_[0] for _ in connection.execute(sql)]
            if tables:
                return [_ for _ in tables]
            return []


class RollBackAndFlush(object):
    def __init__(self):
        pass

    @staticmethod
    def and_execute():
        db.session.rollback()
        db.session.flush()


# noinspection PyUnresolvedReferences,PyMethodMayBeStatic
class HouseKeeping(object):
    def add(self):
        """
        Ability to add and rollback if there's any problem
        :return: None if successful, else, returns the error encountered.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return {}
        except SQLAlchemyError as exc:
            RollBackAndFlush.and_execute()

            # from ast import literal_eval
            # front, back = e.args[0].split(') ')
            # code, msg = literal_eval(back)
            # return {"type": front.replace('(', ''), "code": code, "msg": msg}

            return get_exception_message(exc)

    def named(self):
        return self.__table__.name

    def display(self):
        pprint(loads(json_data(self.__table__.name, self.id)))

    def as_dict(self, bypass=None):
        result = OrderedDict()
        for key in self.__table__.columns.keys():  # OR self.__mapper__.c.keys()
            if bypass != key:
                result[key] = getattr(self, key)
        return result

    def as_json(self):
        return json_data(self.__table__.name, self.id)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.id)

    @classmethod
    def columns(cls):
        return cls.__table__.columns.keys()

    @classmethod
    def relationships(cls):
        """
        Returns a relationship and indicates if it's a list (True) or not
        :return: list
        """
        return [[_, "is_list: {}".format(cls.__mapper__.relationships[_].uselist)] for _ in
                cls.__mapper__.relationships.keys()]

    @classmethod
    def valid_update_attribute(cls):
        # exclude AuditTrail, Validation, Payment
        keys = cls.__mapper__.c.keys()
        all_objects = cls.__dict__
        exclude = ['id', 'added_by', 'added_on', 'modified_on', 'password_hash', 'last_auth_time']

        result = []

        for each in all_objects:
            if isinstance(all_objects[each], InstrumentedAttribute) and each in keys and each not in exclude:
                result.append(each)
        return dict(table_name=cls.__table__.name, can_update=result)

    @classmethod
    def get_field_and_relationships(cls):
        return dict(table_name=cls.__table__.name, columns=cls.columns(), relationships=cls.relationships())


# noinspection PyMethodParameters
class Base(db.Model, HouseKeeping):
    """Base model that other specific models inherit from"""

    __abstract__ = True

    added_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    added_by = db.Column(db.BigInteger, nullable=False, index=True)

    # BigInteger range: -9223372036854775808 to 9223372036854775807
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    enabled = Evolve.create_bool(db, default=True)


def remove_json_unwanted(*args):
    result = args[0]
    for each in args[1:]:
        result.pop(each, None)
    return result


def date_handler(value):
    """
    Return a string type of Python datetime format
    :param value: datetime of Python
    :return: string
    """
    return value.isoformat() if hasattr(value, 'isoformat') else value


# noinspection PyProtectedMember
def get_class_by_tablename(tablename):
    for c in db.Model._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c


# noinspection PyProtectedMember
def json_data(tablename, _id, bypass=None):
    """
    Returns the json representation of a table. It converts any datetime object to a string representation of the time
    :param tablename: The name of the table: User.query.get(1).named()
    :param _id: the id of the table to query
    :param bypass: the attribute to remove
    :return: json format
    """
    try:
        data = get_class_by_tablename(tablename).query.get(_id).as_dict()
        if bypass:
            try:
                data.pop(bypass)
            except KeyError:
                pass
        return dumps(data, default=date_handler)
    except AttributeError:
        return dumps({})


def latest(_class):
    db.engine.echo = False
    try:
        print('\n')
        return _class.query.order_by(_class.id.desc()).first().display()
    except (Exception,) as e:
        RollBackAndFlush.and_execute()
        print('\nNo data found')


# noinspection PyProtectedMember
def show_all():
    classes, models, table_names = [], [], []
    for clazz in db.Model._decl_class_registry.values():
        if hasattr(clazz, '__tablename__'):
            table_names.append(clazz.__tablename__)
            classes.append(clazz)

    for table in db.metadata.tables.items():
        if table[0] in table_names:
            models.append(classes[table_names.index(table[0])])

    return classes, models, table_names


# noinspection PyProtectedMember
def show_classes():
    classes = []
    for the_class in db.Model._decl_class_registry.values():
        if hasattr(the_class, '__tablename__'):
            classes.append(the_class)
    return classes  # classes[0].query.get(1)


# noinspection PyProtectedMember
def get_class(table_name):
    for the_class in db.Model._decl_class_registry.values():
        if hasattr(the_class, '__tablename__'):
            if the_class.__tablename__ == table_name:
                return the_class
    return None


# noinspection PyArgumentList
def compile_query(query):
    dialect = query.session.bind.dialect
    comp = query.statement.compile(dialect=dialect)

    # the one below caused errors with ARRAY types
    # from sqlalchemy.sql import compiler
    # comp = compiler.SQLCompiler(dialect, statement)
    # comp.compile()

    enc = dialect.encoding
    params = {}

    # if app.config['DB_TYPE'] == 'MYSQL':
    #     items = comp.params.items()
    # else:
    #     items = comp.params.iteritems()
    for k, v in comp.params.items():
        if isinstance(v, str):
            v = v.encode(enc)
        params[k] = sqlescape(v)
    return str(comp.string % params)
