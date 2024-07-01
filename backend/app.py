from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

import setting
import gpt
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
    myGPT = gpt.MyGPT(setting.configs)
    msgs = []
    insctruct_prompt = "Your task is to recognize the annotated food ingrediants in the picture. \
        If there is no annotation, recongize all the food ingrediants. \
        As reply only list the recoginzed food ingredients quoted in square brackets and each of them is quoted with double quotes and seperated with a comma. If there are only non-food items recognized, reply me only []"
    user_msg= gpt.GPTMsg('user', insctruct_prompt)
    example_prompt = 'I will give you two examples. \
        Q1: Recognize the annotated food ingrediants in first picture. \
        If there is no annotation, recongize all the food ingrediants. \
        A1: ["aubergine","chicken wings"] \
        Q2: Recognize the annotated food ingrediants in second picture. \
        If there is no annotation, recongize all the food ingrediants. \
        A2: ["aubergine","romaine lettuce","chicken wings","red bell pepper"]'
    example_msg = gpt.GPTMsg('user', example_prompt, [setting.Path(setting.root_dir) / UPLOAD_FOLDER / 'origin' / 'test1.jpg', setting.Path(setting.root_dir) / UPLOAD_FOLDER / 'origin' / 'test2.jpg'])
    task_prompt = 'Q3: Recognize the annotated food ingrediants in second picture. \
        If there is no annotation, recongize all the food ingrediants. \
        A3:'
    task_msg = gpt.GPTMsg('user', task_prompt, [setting.Path(setting.root_dir) / save_path])
    msgs.append(user_msg)
    msgs.append(example_msg)
    msgs.append(task_msg)

    global global_ingredients

    result, reply = gpt.process_response(myGPT.query(msgs), myGPT.model)
    if not result:
        print("Error! See the details below.")
        # return jsonify({"message": reply})
    # TEST: frontend image to backend recipes
    # print(reply)

    global_ingredients = reply
    # END OF TEST: frontend image to backend recipes
    return jsonify({"message": reply})
    # return jsonify({"message": "File successfully uploaded", "filename": file.filename})

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
