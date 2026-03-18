import logging
import secrets
import string
import jwt
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a function to generate a random secret key for JWT
def generate_secret_key():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))

# Define a function to create a new JWT
def create_jwt(user_id, expiry=3600):
    secret_key = generate_secret_key()
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=expiry)
    }
    return jwt.encode(payload, secret_key, algorithm="HS256"), secret_key

# Define a function to verify a JWT
def verify_jwt(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        logger.error("Invalid token.")
        return None

# Define a function to generate a reset password token
def generate_reset_password_token():
    secret_key = generate_secret_key()
    token = secrets.token_urlsafe(32)
    return token, secret_key

# Define a function to verify a password reset token
def verify_reset_password_token(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return True
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired.")
        return False
    except jwt.InvalidTokenError:
        logger.error("Invalid token.")
        return False