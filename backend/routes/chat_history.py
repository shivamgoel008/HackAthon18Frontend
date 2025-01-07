from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from service.chat_history_service import ChatHistoryService

chat_history_bp = Blueprint('chat_history', __name__)

chat_history_service = ChatHistoryService()


@chat_history_bp.route('/chat_history/user', methods=['GET'])
@jwt_required()
def get_all_chats_for_user():
    user_id = get_jwt_identity()
    try:
        return jsonify(chat_history_service.get_all_chats_for_user(user_id=user_id)), 200
    except Exception as e:
        return jsonify({"error": str(e)})


@chat_history_bp.route('/chat_history/chat', methods=['GET'])
@jwt_required()
def get_messages_for_user_chat():
    user_id = get_jwt_identity()
    chat_id = request.args.get('chat_id')
    try:
        return jsonify(chat_history_service.get_messages_for_user_chat(user_id=user_id, chat_id=chat_id)), 200
    except Exception as e:
        return jsonify({"error": str(e)})


@chat_history_bp.route('/chat_history/chat', methods=['POST'])
@jwt_required()
def add_chat_message():
    try:
        data = request.json
        data["user_id"] = get_jwt_identity()
        return jsonify(chat_history_service.add_chat_message(data)), 200
    except Exception as e:
        return jsonify({"error": str(e)})
