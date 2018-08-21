import os

DB_TYPE = os.getenv('DB_TYPE')

if DB_TYPE == 'MYSQL':
    from sqlalchemy.dialects.mysql import JSON

if DB_TYPE == 'POSTGRES':
    from sqlalchemy.dialects.postgresql import JSONB


class Evolve(object):
    def __init__(self):
        pass

    @staticmethod
    def mysql_json():
        return JSON

    @staticmethod
    def postgres_json():
        return JSONB

    @staticmethod
    def create_bool(db, default=False):
        if DB_TYPE == 'MYSQL':
            return db.Column(db.SmallInteger, nullable=False, default=default)

        if DB_TYPE == 'POSTGRES':
            # this works on Postgres but fails on MySQL
            return db.Column(db.Boolean, nullable=False, default=default)

