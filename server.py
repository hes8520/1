from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
USER_FILE = "users.json"
CORS(app)

from flask import send_from_directory

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # 요청한 파일이 현재 폴더에 존재하면 그 파일 반환
    if path != "" and os.path.exists(path):
        return send_from_directory('.', path)
    # 아니면 index.html 반환 (프론트엔드 라우터가 처리)
    return send_from_directory('.', 'index.html')

def load_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, "r", encoding="utf-8") as f:
        users = []
        for line in f:
            if line.strip():
                users.append(json.loads(line))
        return users


def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        for user in users:
            f.write(json.dumps(user, ensure_ascii=False) + "\n")


@app.route("/check_id", methods=["POST"])
def check_id():
    data = request.json
    userid = data.get("userid")
    users = load_users()
    exists = any(u.get("userid") == userid for u in users)
    return jsonify({"exists": exists})


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    userid = data.get("userid")
    password = data.get("password")
    age = data.get("age")
    gender = data.get("gender")
    region = data.get("region")
    interests = data.get("interests", [])

    users = load_users()
    if any(u.get("userid") == userid for u in users):
        return jsonify({"message": "이미 존재하는 아이디입니다."}), 400

    new_user = {
        "userid": userid,
        "password": password,
        "age": age,
        "gender": gender,
        "region": region,
        "interests": interests,
        "isPublic": False
    }
    users.append(new_user)
    save_users(users)
    return jsonify({"message": "회원가입 완료"}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    userid = data.get("userid")
    password = data.get("password")
    users = load_users()
    for u in users:
        if u.get("userid") == userid and u.get("password") == password:
            return jsonify({"message": "로그인 성공"}), 200
    return jsonify({"message": "아이디 또는 비밀번호가 틀렸습니다."}), 401


@app.route("/get_profile", methods=["POST"])
def get_profile():
    data = request.json
    userid = data.get("userid")
    users = load_users()
    for u in users:
        if u.get("userid") == userid:
            return jsonify({"profile": u}), 200
    return jsonify({"message": "프로필이 없습니다."}), 404


@app.route("/update_profile", methods=["POST"])
def update_profile():
    data = request.json
    userid = data.get("userid")

    users = load_users()
    for u in users:
        if u.get("userid") == userid:
            u["age"] = data.get("age", u.get("age"))
            u["gender"] = data.get("gender", u.get("gender"))
            u["region"] = data.get("region", u.get("region"))
            u["interests"] = data.get("interests", u.get("interests"))
            u["isPublic"] = data.get("isPublic", u.get("isPublic"))
            save_users(users)
            return jsonify({"message": "프로필 업데이트 완료"}), 200
    return jsonify({"message": "사용자를 찾을 수 없습니다."}), 404


@app.route("/get_public_profiles", methods=["GET"])
def get_public_profiles():
    users = load_users()
    public_users = [u for u in users if u.get("isPublic")]
    return jsonify({"profiles": public_users}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
