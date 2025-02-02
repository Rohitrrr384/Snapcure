from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os

app = Flask(__name__)

# Load the model (ensure the path is correct)
MODEL_PATH = r"C:/Users/rohit/models/saved_models/mini_project__050.keras"
model = load_model(MODEL_PATH)

# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the uploaded file temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        # Preprocess the image
        img = load_img(file_path, target_size=(32, 32))  # Match your model's input size
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize if the model requires it

        # Make prediction
        predictions = model.predict(img_array)
        class_label = np.argmax(predictions, axis=1)[0]  # Get the highest probability class

        return jsonify({"class_label": int(class_label)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Clean up the saved file
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5001)

