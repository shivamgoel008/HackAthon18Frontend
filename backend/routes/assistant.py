from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from backend.service.chat_service import ChatService

assistant_bp = Blueprint('assistant', __name__)

chatservice = ChatService()


@assistant_bp.route('/query', methods=['POST'])
@jwt_required()
def query_it():
    data = request.json
    query = data.get('query')
    response = chatservice.query(query)
    return jsonify(response), 200
