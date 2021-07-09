import os
from flask import Flask, render_template, request

# Create the app
def create_app(test_config=None):

    # Create the App
    app = Flask(__name__, static_url_path='', template_folder='templates')

    # Configure either from file or from test options
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object('config')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Initialize DataBase Connection

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app