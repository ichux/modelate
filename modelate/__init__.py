import os
import time
from datetime import datetime

from flask import Flask
from flask_migrate import Migrate, init, migrate, revision, upgrade
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from modelate.helpers import date_time_format, AnonymousUser, metadata, get_real_ip, unique_id

app = Flask(__name__, static_folder='statics/non-templates', template_folder='statics/templates', static_url_path='/s')
app.config.from_object(os.getenv('MODELATE_STATUS'))

configs = app.config

db = SQLAlchemy(app, metadata=metadata)
Migrate(app, db)

uploads = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(uploads):
    try:
        os.mkdir(uploads)
    except (Exception,):
        pass

app.jinja_env.cache = {}  # hasten the loading of templates
app.jinja_env.trim_blocks = True  # Removes unwanted whitespace from render_template function


class Usable(object):
    def __init__(self):
        self.time = datetime.utcfromtimestamp(time.time())
        self.directory = os.path.join(os.getcwd(), 'migrations', 'versions')

    def message(self):
        return self.time.strftime("%Y_%m_%d")

    def revision_id(self):
        path, dirs, files = next(os.walk(self.directory))
        return str(len([file_ for file_ in files if file_.endswith('.py')]) + 1).zfill(4)


@app.shell_context_processor
def make_shell_context():
    from modelate.models.profiling import User
    return dict(app=app, db=db, User=User)


@app.cli.command("dbi")
def dbi():
    """
    Calls the init()
    :return: None
    """
    init()


@app.cli.command("dbm")
def dbm():
    """
    Calls the migrate()
    :return: None
    """
    usable = Usable()
    migrate(message=usable.message(), rev_id=usable.revision_id())


@app.cli.command("dbr")
def dbr():
    """
    Calls the revision()
    :return: None
    """
    usable = Usable()
    revision(message=usable.message(), rev_id=usable.revision_id())


@app.cli.command("dbu-sql")
def dbu_sql():
    """
    Generate SQL statements but you will personally have to `run` it on your DB
    :return: None
    """
    upgrade(sql=True)


@app.cli.command("dbu-no-sql")
def dbu_no_sql():
    """
    Bring the DB up to date with your data models.
    Calls the migrate()
    :return: None
    """
    upgrade()


csrf = CSRFProtect(app)

from modelate.models.profiling import User
from modelate.controllers.apiv1 import apiv1
from modelate.controllers.frontend import frontend

app.register_blueprint(frontend)
app.register_blueprint(apiv1, url_prefix='/api/v1.0')

# exempt API routes from csrf checks
csrf.exempt(apiv1)
