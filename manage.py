import os
import time
from datetime import datetime

from flask_migrate import init, migrate, revision, upgrade
from flask_script import Shell

from modelate import manager, app, db
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


if __name__ == '__main__':
    manager.run()
