from flask import Flask, render_template, request, jsonify
import os
import face_recognition
import base64
import pickle

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register')
def register_page():
    return render_template("register.html")

@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    image_data = data.get('image')

    if not name or not image_data:
        return jsonify({"status": "error", "message": "Missing name or image"}), 400

    os.makedirs("saved_faces", exist_ok=True)
    os.makedirs("encodings", exist_ok=True)

    header, encoded = image_data.split(",", 1)
    image_bytes = base64.b64decode(encoded)
    temp_path = os.path.join("saved_faces", f"{name}_temp.jpg")

    with open(temp_path, "wb") as f:
        f.write(image_bytes)

    image = face_recognition.load_image_file(temp_path)
    encodings = face_recognition.face_encodings(image)

    if not encodings:
        return jsonify({"status": "error", "message": "No face found!"}), 400

    with open(f"encodings/{name}.pkl", "wb") as f:
        pickle.dump(encodings[0], f)

    os.remove(temp_path)
    return jsonify({"status": "success", "message": "Registration successful!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    image_data = data.get('image')

    if not image_data:
        return jsonify({"status": "error", "message": "No image provided"}), 400

    header, encoded = image_data.split(",", 1)
    image_bytes = base64.b64decode(encoded)
    temp_path = os.path.join("saved_faces", "login_temp.jpg")

    with open(temp_path, "wb") as f:
        f.write(image_bytes)

    unknown_image = face_recognition.load_image_file(temp_path)
    unknown_encodings = face_recognition.face_encodings(unknown_image)

    if not unknown_encodings:
        return jsonify({"status": "error", "message": "No face detected"}), 400

    unknown_encoding = unknown_encodings[0]

    for file in os.listdir("encodings"):
        with open(os.path.join("encodings", file), "rb") as f:
            known_encoding = pickle.load(f)
        match = face_recognition.compare_faces([known_encoding], unknown_encoding)[0]
        if match:
            name = file.replace(".pkl", "")
            return jsonify({"status": "success", "message": f"Welcome, {name}!"})

    return jsonify({"status": "error", "message": "No match found"})
if __name__ == "__main__":
    app.run(debug=True)


