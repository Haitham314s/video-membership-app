import secrets
from datetime import datetime, timedelta

from jose import jwt, ExpiredSignatureError

from .models import User
from app.config import get_settings

secret_key = secrets.token_urlsafe(50)
algo = "HS256"
settings = get_settings()


def authenticate(email, password):
    try:
        user_obj = User.objects.get(email=email)
    except Exception as e:
        user_obj = None

    return user_obj if user_obj.verify_password(password) else None


def login(user_obj, expires=5):
    return jwt.encode({
        "user_id": f"{user_obj.user_id}",
        "email": "do not do this",
        "exp": datetime.utcnow() + timedelta(seconds=expires)
    }, settings.secret_key, algorithm=settings.algo)


def verify_user_id(token):
    data = {}
    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[settings.algo])
    except ExpiredSignatureError as e:
        print(e)
    except Exception:
        pass

    return None if "user_id" not in data else data
