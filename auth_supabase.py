"""
Supabase JWT verification and user id extraction for API routes.
"""
import os
import jwt
from functools import wraps
from flask import request, jsonify

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET")


def get_user_id_from_request():
    """
    Read Authorization: Bearer <token>, verify Supabase JWT, return user id (uuid) or None.
    """
    if not SUPABASE_JWT_SECRET:
        return None
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return None
    token = auth[7:].strip()
    if not token:
        return None
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
            options={"verify_aud": False},
        )
        return payload.get("sub")
    except Exception:
        return None


def require_auth(f):
    """Decorator: return 401 if no valid user."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        user_id = get_user_id_from_request()
        if not user_id:
            return jsonify({"error": "Unauthorized", "message": "Sign in required"}), 401
        return f(user_id, *args, **kwargs)
    return wrapped
