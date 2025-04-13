import jwt
from src.database import get_user_by_email_or_phone
from src.utils import generate_token
import datetime

SECRET_KEY = 'your_secret_key'

def create_jwt_token(user_id):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'user_id': user_id,
        'exp': expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_jwt_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def authenticate_user(username, password):
    user = get_user_by_email_or_phone(username)
    if user:
        stored_token = user[4]
        if generate_token(username, password) == stored_token:
            return True
    return False
