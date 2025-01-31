import os
import pickle
import joblib
import numpy as np
import cv2
from flask import Flask,render_template,request

from tensorflow import keras
model_ct = keras.models.load_model('prediction-ct.h5')
UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['imagefile']
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        predict_ct = [] 
        img = cv2.imread('static/uploads/'+file.filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(gray,(150,150))
        predict_ct.append(img)
        predict_ct = np.array(predict_ct)
        predict_ct = predict_ct.reshape(predict_ct.shape[0], 150, 150,1)

        predict_x=model_ct.predict(predict_ct) 
        classes_x=np.argmax(predict_x, axis=1)
        classes_x
        if classes_x[0]==0:
            x='Your CT Scan is Normal!'
            print(x)
        else:
            x='You are suffering from Pneumonia.'
            print(x)
    return render_template('home.html', val=x)


if __name__ == '__main__':
    app.run()
