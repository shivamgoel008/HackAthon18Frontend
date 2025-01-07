import os

from flask import Flask
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp
from routes.assistant import assistant_bp
from routes.chat_history import chat_history_bp

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
jwt = JWTManager(app)
app.register_blueprint(auth_bp)
app.register_blueprint(assistant_bp)
app.register_blueprint(chat_history_bp)

if __name__ == '__main__':
    app.run(debug=True)