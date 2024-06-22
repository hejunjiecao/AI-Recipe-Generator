from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

import setting
import gpt

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
save_path = ''

@app.route("/upload", methods=["POST"])
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
        As answer you generate a JSON object with their names as keys and their quantity as values."
    user_msg= gpt.GPTMsg('user', insctruct_prompt)
    example_prompt = 'I will give you one example. \
        Q1: Recognize the annotated food ingrediants in the first picture. \
            If there is no annotation, recongize all the food ingrediants. \
        A1: {"aubergine": "1 piece", "chicken wings": "600 gram"} \
        Q2: Recognize the annotated food ingrediants in the second picture. \
            If there is no annotation, recongize all the food ingrediants. \
        A2:{"aubergine": "1 piece","romaine lettuce": "3 pieces","chicken wings": "600 grams","red bell pepper": "1 piece"}'
    example_msg = gpt.GPTMsg('user', example_prompt, [setting.Path(setting.root_dir) / UPLOAD_FOLDER / 'origin' / 'test1.jpg', setting.Path(setting.root_dir) / UPLOAD_FOLDER / 'origin' / 'test2.jpg'])
    task_prompt = 'Q1: Recognize the annotated food ingrediants in the first picture. \
        If there is no annotation, recongize all the food ingrediants. \
        A1:'
    task_msg = gpt.GPTMsg('user', task_prompt, [setting.Path(setting.root_dir) / save_path])
    msgs.append(user_msg)
    msgs.append(example_msg)
    msgs.append(task_msg)

    result, reply = gpt.process_response(myGPT.query(msgs), myGPT.model)
    if not result:
        print("Error! See the deatils below.")
        return jsonify({"message": reply})
    print(reply)
    return jsonify({"message": reply})
    # return jsonify({"message": "File successfully uploaded", "filename": file.filename})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
