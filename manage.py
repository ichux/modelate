import os
import secrets
import time
from datetime import datetime
from urllib.parse import unquote

from flask_migrate import init, migrate, revision, upgrade
from flask_script import Shell, prompt_bool

from modelate import manager, app, db
from modelate.models import QueryPostgres
from modelate.models.profiling import User


class Usable(object):
    def __init__(self):
        self.time = datetime.utcfromtimestamp(time.time())
        self.directory = os.path.join(os.getcwd(), 'migrations', 'versions')

    def message(self):
        return self.time.strftime("%Y_%m_%d")

    def revision_id(self):
        path, dirs, files = next(os.walk(self.directory))
        return str(len([file_ for file_ in files if file_.endswith('.py')]) + 1).zfill(4)


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def dbi():
    """
    Calls the init()
    :return: None
    """
    init()


@manager.command
def dbm():
    """
    Calls the migrate()
    :return: None
    """
    usable = Usable()
    migrate(message=usable.message(), rev_id=usable.revision_id())


@manager.command
def dbr():
    """
    Calls the revision()
    :return: None
    """
    usable = Usable()
    revision(message=usable.message(), rev_id=usable.revision_id())


@manager.command
def dbu_sql():
    """
    Generate SQL statements but you will personally have to `run` it on your DB
    :return: None
    """
    upgrade(sql=True)


@manager.command
def dbu_no_sql():
    """
    Bring the DB up to date with your data models.
    Calls the migrate()
    :return: None
    """
    upgrade()


# noinspection SqlDialectInspection
@manager.command
def drop_pg_tables(namespace="'public'"):
    """For dropping Postgres the tables."""
    status = os.environ.get('SERVER_STATUS')
    if status != 'live':  # status != 'production' or
        if prompt_bool("Are you sure you want to lose all DB data?\n'y', 'yes', '1', 'on', 'true', 't' "
                       "OR 'n', 'no', '0', 'off', 'false', 'f': "):

            db.engine.echo = True
            tables = QueryPostgres.get_postgres_tables(namespace)

            if tables:
                with db.engine.connect() as connection:
                    connection.execute(f"DROP TABLE {', '.join(tables)} CASCADE")
                    print('all tables have been dropped')
        else:
            print('\n*** You cancelled the operation ***')
    else:
        print('\n*** You can not drop_all on PRODUCTION server! What were you thinking?***')


@manager.command
def sitemap():
    """
    List all the site maps of your application
    :return: None
    """
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        output.append(unquote(f"{rule.endpoint:30s} {methods:25s} {rule}"))

    for _ in sorted(output):
        print(_)


@manager.command
def locate_route(check):
    """
    Based on what you probably got from using `sitemap` function, narrow down to a route with this function
    :param check: value to check if it's in a route
    :return: None
    """
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)

        if check in rule.endpoint:
            output.append(unquote(f"{rule.endpoint:30s} {methods:25s} {rule}"))

    for _ in sorted(output):
        print(_)


@manager.command
def bits_256():
    """
    Generate a random number of length 256 bits
    :return: number
    """
    # import Crypto.Random.random
    # print(Crypto.Random.random.getrandbits(256))

    print(secrets.randbits(256))


if __name__ == '__main__':
    manager.run()
