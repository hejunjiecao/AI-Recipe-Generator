from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/upload", methods=["POST"])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)
    
    return jsonify({"message": "File successfully uploaded", "filename": file.filename})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/recipe', methods=['GET'])
def get_recipe():
    recipe = {
        "name": "鱼香肉丝",
        "totalTime": "30分钟",
        "ingredients": [
            {"name": "猪肉", "amount": "200g"},
            {"name": "青椒", "amount": "100g"},
            {"name": "胡萝卜", "amount": "50g"}
        ],
        "steps": [
            "将猪肉切丝。",
            "将青椒和胡萝卜切丝。",
            "锅中放油，加入猪肉炒熟。",
            "加入青椒和胡萝卜，翻炒均匀。"
        ]
    }
    return jsonify(recipe)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)