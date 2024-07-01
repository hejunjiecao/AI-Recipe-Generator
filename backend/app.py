from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

import recognizer as recog
import recipe_generator as rcp_gen

app = Flask(__name__)
CORS(app)

# global_ingredients = {}
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

    # 将文件保存到本地
    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    # 打印保存路径
    print(f"File saved to: {save_path}")

	# recognize
    global global_ingredients
    reply = recog.recognize_food_ingredients(UPLOAD_FOLDER, save_path)
    global_ingredients = reply

    return jsonify({"message": reply})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/generate", methods=["GET"])
def generate_recipe():
    # TODO: Assume the data contains a dictionary of ingredients
    # example:
    # {"style": "chinese", "ingredients": ["tomato","salad"]}

    # TEST: frontend image to backend recipes
    # data = request.get_json()

    # data = global_ingredients
    data = '["grapes","tofu","cheese spread"]'
    # if not data:
    #     return jsonify({"error": "No input data provided"}), 400
    # style = data.get("style",{})
    # if not style:
    #     style = "any"
    style = "any"


    # data = dirty_data.replaceAll("`","")
    # data = data.replace("json","")
    # data = {"tomato": "2 pieces", "cheese": "100 grams"}
    # END OF TEST: frontend image to backend recipes


    # Process ingredients to generate a recipe
    three_recipes = rcp_gen.generate_recipe_from_ingredients(data, style)
    # # TEST: frontend image to backend recipes
    # # print(three_recipes[0])
    # # print(type(three_recipes[0]))
    # # recipe = three_recipes[0].replace("'", '"')
    three_recipe_objs = []
    for i in range(3):
        cleaned = three_recipes[i][7:-3]
        # print(cleaned)
        three_recipe_objs.append(json.loads(cleaned))
    # # test_recipe = three_recipes[0]
    # # test_obj.ingredients = data
    # return jsonify(test_obj)
    # # END OF TEST: frontend image to backend recipes
    return jsonify({"recipes": three_recipe_objs})


    # return jsonify({"recipe": three_recipes[0]})

# TEST: recipe_generator
@app.route("/")
def home():
    return send_from_directory('spec', 'recipe_gen.html')
# END OF TEST: recipe_generator

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5008, debug=True)
