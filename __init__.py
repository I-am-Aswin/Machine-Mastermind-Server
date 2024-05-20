import os
import tensorflow as tf
from flask import Flask
from flask import ( render_template, url_for )
from . import views
from . import config

test_config = None

app = Flask( __name__, instance_relative_config=True )

if test_config is not None:
    app.config.from_mapping( test_config )
else:
    app.config.from_object( config.Config )

app.config['BASE_DIR'] = __name__
os.makedirs( app.config['UPLOAD_FOLDER'], exist_ok=True )
os.makedirs(app.instance_path, exist_ok=True)

app.register_blueprint( views.app )