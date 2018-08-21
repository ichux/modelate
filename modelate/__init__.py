from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

import modelate.bootstrap
from modelate.helpers import date_time_format, AnonymousUser, metadata, get_real_ip, unique_id
from modelate.setup import app_configuration

app = Flask(__name__, static_folder='statics/nontemplate', template_folder='statics/templates', static_url_path='/s')
app_configuration(app)  # adds the configuration and does some setup too
configs = app.config

db = SQLAlchemy(app, metadata=metadata)
Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

csrf = CSRFProtect(app)

from modelate.controllers.apiv1 import apiv1
from modelate.controllers.frontend import frontend

app.register_blueprint(frontend)
app.register_blueprint(apiv1, url_prefix='/api/v1.0')

# exempt API routes from csrf checks
csrf.exempt(apiv1)
