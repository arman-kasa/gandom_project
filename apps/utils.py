from flask import abort
from apps import redisClient
from apps.model.user import User


def get_user_by_token(token):
    try:
        username = redisClient.get(token).decode("utf-8")
        user = User.objects(username=username).first()
        return user.username
    except Exception:
        abort(401)
