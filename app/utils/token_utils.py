import os
import jwt
import datetime
from flask import request, jsonify
from functools import wraps
from dotenv import load_dotenv
from ..models import User


dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")
load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY: 
    raise ValueError("SECRET_KEY não foi encontrada. Certifique-se de que o arquivo .env está configurado corretamente.")


def generate_token(user):
    token = jwt.encode(
        {
            "id": user.id,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return token


def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token não encontrado!"}), 403

        try:
            data = decode_token(token.split(" ")[1])  
            current_user = User.query.get(data["id"])
        except Exception as e:
            return jsonify({"message": "Token inválido ou expirado!", "error": str(e)}), 403

        return f(current_user, *args, **kwargs)

    return decorated
