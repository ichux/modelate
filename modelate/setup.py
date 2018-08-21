import os

# BASE_DIRECTORY = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

MODELATE_STATUS = os.getenv('MODELATE_STATUS')
UPLOADS = os.path.join(os.getcwd(), 'uploads')


def app_configuration(app):
    """
    Sets up the application configuration
    :param app: the application
    :return: None
    """

    if MODELATE_STATUS == 'development':
        app.config.from_object('modelate.config.DevelopmentConfig')
        print(f'modelate_status: {MODELATE_STATUS}\n')
    elif MODELATE_STATUS == 'live':
        app.config.from_object('modelate.config.LiveConfig')
        print(f'modelate_status: {MODELATE_STATUS}\n')
    else:
        app.config.from_object('modelate.config.TestConfig')
        print('modelate_status: test\n')

    # create non existent uploads directory
    if not os.path.exists(UPLOADS):
        try:
            os.mkdir(UPLOADS)
        except (Exception,):
            pass

    # Ensure gen directory used by `assets` exists
    # assets_output_dir = os.path.join(app.root_path, 'statics', 'nontemplate', 'gen')
    # if not os.path.exists(assets_output_dir):
    #     try:
    #         os.makedirs(assets_output_dir, exist_ok=True)
    #     except (Exception,):
    #         pass

    # app.jinja_env.filters['date_time_format'] = date_time_format
    app.jinja_env.cache = {}  # hasten the loading of templates
    app.jinja_env.trim_blocks = True  # Removes unwanted whitespace from render_template function
