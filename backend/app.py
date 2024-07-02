from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

import setting
import gpt
import recipe_generator as rcp_gen

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
save_path = ''
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/uploads", methods=["POST"])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"})

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    print(f"File saved to: {save_path}")
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Assume the data contains a dictionary of ingredients
    # example:
    # {"tomato": "2 pieces", "cheese": "100 grams"}
    # ingredients = data.get("ingredients", {})

    # if not ingredients:
    #     return jsonify({"error": "No ingredients provided"}), 400

@app.route("/generate", methods=["POST"])
def generate_recipe():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    style = data.get("style",{})

    if not style:
        style = "any"
    # Process ingredients to generate a recipe
    recipe = rcp_gen.generate_recipe_from_ingredients(data, style)

    return jsonify({"recipe": recipe})

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5008, debug=True)
