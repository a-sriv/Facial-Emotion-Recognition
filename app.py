import os
import numpy as np
import tensorflow as tf
import PIL
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

app.config["IMAGE_UPLOADS"]='IMAGE_UPLOADS'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if request.files:
            image = request.files['image']
            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['IMAGE_UPLOADS'], filename))
                
                
                check = Image.open(image)
                check = check.convert('L')
                resized_img = check.resize((48,48))
                array = np.array(resized_img)
                array = array/255.0
                reshaped_array = array.reshape(1,48,48,1)

                model = tf.keras.models.load_model(r'model.h5')

                output = model.predict(reshaped_array)
                
                
                #Mapping for prediction We have output[i] then (i=0 -> Happy, i=1 -> Neutral, i=2 -> Sad

                output_list = output[0][:]
                output_list = output_list.tolist()

            
                max_value_index = output_list.index(max(output_list))

                if max_value_index==0:
                    expression = 'Happy'

                if max_value_index==1:
                    expression = 'Neutral'

                if max_value_index==2:
                    expression = 'Sad'  

                else :
                    print("Data Incorrect") 
                    
            

                
    

                

            else:
                print("That file extension is not allowed")
                return redirect(request.url)

    
        return render_template('predict.html', prediction_text = "Result of Analysis : Facial Analysis suggests the person is {}".format(expression))



if __name__=='__main__':
    app.run(debug=True)