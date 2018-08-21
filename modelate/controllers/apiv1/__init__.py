from flask import Blueprint

apiv1 = Blueprint('apiv1', __name__)
from modelate.controllers.apiv1 import apiv1_view


@apiv1.before_request
def v1_api_before_request():
    """
    This will occur after the main app's 'before request' has been called.

    Note: this will not be called on routes registered on the app e.g.
    @app.route('/api/v1.0/auth/', methods=["POST"])

    But will be called on routes like this: @v1_api.route('/')
    """
    pass


@apiv1.after_request
def per_request_callbacks(response):
    # response.headers['Last-Modified'] = datetime.now()
    # response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    # response.headers['Pragma'] = 'no-cache'
    # response.headers['Expires'] = '-1'
    # response.cache_control.no_cache = True
    # response.set_cookie('sessionID', '', expires=0)

    # response.headers['Server'] = ''  # you can't remove it, so, set it to empty
    return response
