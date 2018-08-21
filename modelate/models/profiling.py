from datetime import datetime

from modelate import db
from modelate.models import Base
from modelate.models.db_extra import Evolve


# noinspection PyMethodMayBeStatic,PyCallByClass
class User(Base):
    __tablename__ = 'users'

    last_auth_time = db.Column(db.DateTime)
    username = db.Column(db.String(32), index=True, nullable=False, unique=True)
    roles = db.Column(Evolve.postgres_json())
    multi_roles = Evolve.create_bool(db, default=False)

    hashed_password = db.Column(db.String(250), nullable=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def ping(self):
        self.last_auth_time = datetime.utcnow()
        db.session.add(self), db.session.commit()
