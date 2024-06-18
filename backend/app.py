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
    myGPT = MyGPT(configs)
    user_msgs = generate_user_msg(save_path)
    response = myGPT.query(user_msgs)

    # return jsonify({"message": response['choices'][0]['message']['content']})
    return jsonify({"message": "File successfully uploaded", "filename": file.filename})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
