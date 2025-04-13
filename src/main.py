import jwt
import datetime

SECRET_KEY = 'your_secret_key'

# Function to create JWT token after successful login
def create_jwt_token(user_id):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'user_id': user_id,
        'exp': expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Function to verify JWT token
def verify_jwt_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded['user_id']  # Returns user ID if token is valid
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
