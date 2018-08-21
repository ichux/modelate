from flask import render_template

from modelate.controllers.frontend import frontend


# noinspection PyUnresolvedReferences
@frontend.route('/')
def index():
    return render_template('frontend/index.html')
