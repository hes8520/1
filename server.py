from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

region_distance_order = {
    "서울": {
        "서울": 0, "경기": 1, "인천": 2, "충남": 3, "강원": 4, "세종": 5, "충북": 6,
        "대전": 7, "전북": 8, "전남": 9, "대구": 10, "경북": 11, "부산": 12, "경남": 13,
        "울산": 14, "광주": 15, "제주": 99
    },
    "경기": {
        "경기": 0, "서울": 1, "인천": 2, "강원": 3, "충북": 4, "충남": 5, "세종": 6,
        "대전": 7, "전북": 8, "전남": 9, "경북": 10, "대구": 11, "경남": 12, "부산": 13,
        "울산": 14, "광주": 15, "제주": 99
    },
    "인천": {
        "인천": 0, "경기": 1, "서울": 2, "충남": 3, "강원": 4, "충북": 5, "세종": 6,
        "대전": 7, "전북": 8, "경북": 9, "전남": 10, "대구": 11, "경남": 12, "부산": 13,
        "울산": 14, "광주": 15, "제주": 99
    },
    "강원": {
        "강원": 0, "경기": 1, "서울": 2, "충북": 3, "경북": 4, "충남": 5, "대전": 6,
        "세종": 7, "인천": 8, "전북": 9, "대구": 10, "전남": 11, "경남": 12, "울산": 13,
        "부산": 14, "광주": 15, "제주": 99
    },
    "충북": {
        "충북": 0, "충남": 1, "세종": 2, "대전": 3, "경기": 4, "강원": 5, "서울": 6,
        "전북": 7, "경북": 8, "인천": 9, "대구": 10, "전남": 11, "경남": 12, "부산": 13,
        "울산": 14, "광주": 15, "제주": 99
    },
    "충남": {
        "충남": 0, "세종": 1, "대전": 2, "충북": 3, "경기": 4, "서울": 5, "전북": 6,
        "전남": 7, "인천": 8, "강원": 9, "광주": 10, "경북": 11, "대구": 12, "경남": 13,
        "부산": 14, "울산": 15, "제주": 99
    },
    "세종": {
        "세종": 0, "충남": 1, "충북": 2, "대전": 3, "경기": 4, "서울": 5, "전북": 6,
        "전남": 7, "경북": 8, "강원": 9, "경남": 10, "대구": 11, "부산": 12, "울산": 13,
        "인천": 14, "광주": 15, "제주": 99
    },
    "대전": {
        "대전": 0, "세종": 1, "충남": 2, "충북": 3, "전북": 4, "경기": 5, "서울": 6,
        "강원": 7, "전남": 8, "광주": 9, "경북": 10, "대구": 11, "경남": 12, "부산": 13,
        "울산": 14, "인천": 15, "제주": 99
    },
    "전북": {
        "전북": 0, "충남": 1, "광주": 2, "전남": 3, "세종": 4, "충북": 5, "경기": 6,
        "경남": 7, "대전": 8, "서울": 9, "경북": 10, "부산": 11, "울산": 12, "대구": 13,
        "강원": 14, "인천": 15, "제주": 99
    },
    "전남": {
        "전남": 0, "광주": 1, "전북": 2, "충남": 3, "경남": 4, "부산": 5, "울산": 6,
        "대전": 7, "세종": 8, "경북": 9, "대구": 10, "충북": 11, "경기": 12, "서울": 13,
        "인천": 14, "강원": 15, "제주": 99
    },
    "광주": {
        "광주": 0, "전남": 1, "전북": 2, "충남": 3, "경남": 4, "부산": 5, "울산": 6,
        "대전": 7, "경북": 8, "대구": 9, "충북": 10, "세종": 11, "경기": 12, "서울": 13,
        "인천": 14, "강원": 15, "제주": 99
    },
    "경북": {
        "경북": 0, "대구": 1, "강원": 2, "충북": 3, "경남": 4, "전북": 5, "대전": 6,
        "전남": 7, "울산": 8, "부산": 9, "세종": 10, "충남": 11, "광주": 12, "경기": 13,
        "서울": 14, "인천": 15, "제주": 99
    },
    "경남": {
        "경남": 0, "부산": 1, "울산": 2, "대구": 3, "전북": 4, "경북": 5, "전남": 6,
        "광주": 7, "충남": 8, "대전": 9, "세종": 10, "충북": 11, "경기": 12, "서울": 13,
        "인천": 14, "강원": 15, "제주": 99
    },
    "대구": {
        "대구": 0, "경북": 1, "경남": 2, "울산": 3, "부산": 4, "전북": 5, "광주": 6,
        "전남": 7, "충북": 8, "충남": 9, "세종": 10, "대전": 11, "경기": 12, "서울": 13,
        "인천": 14, "강원": 15, "제주": 99
    },
    "부산": {
        "부산": 0, "경남": 1, "울산": 2, "대구": 3, "전남": 4, "광주": 5, "경북": 6,
        "전북": 7, "충남": 8, "대전": 9, "세종": 10, "충북": 11, "경기": 12, "서울": 13,
        "인천": 14, "강원": 15, "제주": 99
    },
    "울산": {
        "울산": 0, "부산": 1, "경남": 2, "대구": 3, "경북": 4, "전남": 5, "전북": 6,
        "광주": 7, "충남": 8, "대전": 9, "세종": 10, "충북": 11, "경기": 12, "서울": 13,
        "인천": 14, "강원": 15, "제주": 99
    },
    "제주": {
        "제주": 0, "부산": 10, "전남": 11, "경남": 12, "광주": 13, "전북": 14, "서울": 15,
        "경기": 16, "울산": 17, "인천": 18, "충남": 19, "대전": 20, "대구": 21, "세종": 22,
        "충북": 23, "경북": 24, "강원": 25
    }
}



app = Flask(__name__)
USER_FILE = "users.json"
CORS(app)

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
        try:
            return json.load(f)  # 전체 JSON 배열 불러오기
        except json.JSONDecodeError:
            return []

def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

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
    name = data.get("name") 
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
         "name": name,
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
            return jsonify({"message": "로그인 성공", "name": u.get("name")}), 200  # ✅ 이름 포함
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


# --- Ranking 기능 추가 ---

def parse_rankings(data):
    # data: { ageRank, genderRank, locationRank, hobbyRank, preferredGender }
    # 1~4 숫자를 1순위가 가장 높은 값이 되도록 key값으로 변환
    ranks = {
        'age': int(data.get('ageRank')),
        'location': int(data.get('locationRank')),
        'hobby': int(data.get('hobbyRank')),
    }
    preferred_gender = data.get('preferredGender')
    return ranks, preferred_gender

def region_distance_score(user_region, requester_region):
    return region_distance_order.get(requester_region, {}).get(user_region, 99)


def make_sort_key(user, ranks, preferred_gender, requester_region, requester_age, requester_hobbies):
    age_score = abs(int(user.get('age', 0)) - requester_age)
    location_score = region_distance_score(user.get('region'), requester_region)
    user_hobbies = set(user.get('interests', []))
    shared_hobby_count = len(user_hobbies & requester_hobbies)
    hobby_score = -shared_hobby_count

    rank_to_score = {
        ranks['age']: age_score,
        ranks['location']: location_score,
        ranks['hobby']: hobby_score,
    }

    sort_key = tuple(rank_to_score[i] for i in range(1, 4))  # 1~3위까지 정렬
    return sort_key

@app.route('/save_ranking', methods=['POST'])
def save_ranking():
    data = request.json
    ranks, preferred_gender = parse_rankings(data)
    users = load_users()
    requester_userid = data.get('userid')
    requester_region = None
    requester_age = None
    requester_hobbies = set()
    # 요청자 프로필 정보에서 지역, 나이 구하기
    for u in users:
        if u.get('userid') == requester_userid:
            requester_region = u.get('region')
            try:
                requester_age = int(u.get('age', 0))
            except (ValueError, TypeError):
                requester_age = 0
            requester_hobbies = set(u.get('interests') or [])
            break

    filtered_users = [
    u for u in users
    if (
        u.get('isPublic', False)
        and u.get('userid') != requester_userid
        and (
            preferred_gender == "성별무관" or u.get('gender') == preferred_gender
        )
    )
]

    # requester_age가 None 이면 기본값 0 으로 하여 정렬 가능하도록
    if requester_age is None:
        requester_age = 0

    filtered_users.sort(key=lambda u: make_sort_key(u, ranks, preferred_gender, requester_region, requester_age, requester_hobbies ))

    result = []
    for u in filtered_users:
        result.append({
            'name': u.get('name'),
            'age': u.get('age'),
            'gender': u.get('gender'),
            'region': u.get('region'),
            'interests': u.get('interests'),
        })

    return jsonify(success=True, users=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)