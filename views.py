import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image # type: ignore
from flask import ( Blueprint, render_template, request, current_app, url_for )
from werkzeug.utils import secure_filename

app = Blueprint( 'home', __name__, url_prefix='/')

model = None
class_names = ['CSK', 'DC', 'GT', 'KKR', 'LSG', 'MI', 'PBKS', 'RCB', 'RR', 'SRH']

@app.before_app_request
def load_model():
    global model
    if model is None:
        model = tf.keras.models.load_model ( os.path.join( current_app.root_path, r'.\model\MM_Model.keras'))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.post('/predict')
def predict():
    try :
        if 'file' not in request.files:
            return {
                'ok': False,
                'message': 'No Files part Received'
            }
        
        file = request.files['file']
        if file.filename == '':
            return {
                'ok': False,
                'message': 'No Files Selected'
            }
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            img = image.load_img( filepath, target_size = (224, 224))
            img_array = image.img_to_array(img)
            img_array = tf.expand_dims( img_array, 0 )

            predictions = model.predict( img_array )
            class_name = class_names[ np.argmax( predictions ) ]
            confidence = np.max( predictions )

            os.remove(filepath)
            
            return {
                'ok': True,
                'class_name': f'{class_name}',
                'confidence': f'{confidence:.2%}',
                'message': 'Prediction Made Successfully'
            }
    except Exception as e:
        print("Error Occured {}".format(e))
        return {
            'ok':False
        }