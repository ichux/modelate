from flask import Blueprint

frontend = Blueprint('frontend', __name__)

from modelate.controllers.frontend import frontend_view


@frontend.before_request
def frontend_before_request():
    """This will occur after the app's 'before request' has been called.."""
    pass


"""
@frontend.after_request
def frontend_after_request(rv):
    headers = getattr(g, 'headers', {})
    rv.headers.extend(headers)
    return rv
"""
