from datetime import datetime, timedelta, timezone

from jose import jwt, ExpiredSignatureError

from app import config
from .models import User

settings = config.get_settings()


def authenticate(email, password):
    try:
        user_obj = User.objects.get(email=email)
    except Exception as e:
        user_obj = None

    return user_obj if user_obj.verify_password(password) else None


def login(user_obj, expires=settings.session_duration):
    raw_data = {
        "user_id": f"{user_obj.user_id}",
        "role": "admin",
        "exp": datetime.now(timezone.utc) + timedelta(seconds=expires),
    }

    return jwt.encode(raw_data, settings.secret_key, algorithm=settings.jwt_algorithm)


def verify_user_id(token):
    data = {}

    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except ExpiredSignatureError as e:
        print(e, "log out user")
    except Exception:
        pass

    return None if 'user_id' not in data else data
