from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from backend.database.user import UserRepository

auth_bp = Blueprint('auth', __name__)
userRepository = UserRepository()


@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # user = userRepository.authenticate(username, password)
    user = userRepository.get_by_username(username)
    if user:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message='Invalid username or password'), 401


@auth_bp.route('/register', methods=['POST'])
def register():
    data = {
        "username": request.json.get('username'),
        "password": request.json.get('password')
    }
    return jsonify(userRepository.create_new_user(data)), 200


@auth_bp.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    user_identity = get_jwt_identity()
    response = jsonify(message=f'User {user_identity} logged out successfully')
    unset_jwt_cookies(response)
    return response, 200
