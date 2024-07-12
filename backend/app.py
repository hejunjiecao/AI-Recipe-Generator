from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import re

import recognizer as recog
import recipe_generator as rcp_gen

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/uploads", methods=["POST"])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)
    # print(f"File saved to: {save_path}")

    try:
        reply = recog.recognize_food_ingredients(UPLOAD_FOLDER, save_path)
        print(f"Recognized ingredients: {reply}")  # 打印识别的ingredients
        return jsonify({"ingredients": reply})  # 确保返回的数据键名为ingredients
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/generate", methods=["POST"])
def generate_recipe():

    # Assume the data contains a dictionary of ingredients
    # example:
    # {"style": "chinese", "ingredients": ["tomato","salad"]}
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    style = data.get("style",{})
    if not style:
        style = "any"

    ingredients = data.get("ingredients", {})
    if not ingredients:
        ingredients = "[]"

    # Process ingredients to generate a recipe
    three_recipes = rcp_gen.generate_recipe_from_ingredients(data, style)
    three_recipe_objs = []
    for i in range(3):
        cleaned = three_recipes[i][7:-3].replace("'", '"')
        print("cleaned:!!!!")
        print(cleaned)
        three_recipe_objs.append(json.loads(cleaned))
    return jsonify({"recipes": three_recipe_objs})

# TEST: recipe_generator
@app.route("/")
def home():
    return send_from_directory('spec', 'recipe_gen.html')
# END OF TEST: recipe_generator

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)
