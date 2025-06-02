from functools import wraps

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from users.models import User


# CBV驗證裝飾器
def token_required_cbv(view_func):
    @wraps(view_func)
    def warpper(self, request, *args, **kwargs):
        raw_token = request.COOKIES.get("auth_token")
        if not raw_token or ":" not in raw_token:
            return Response(
                {"error": "未提供 Token"}, status=status.HTTP_401_UNAUTHORIZED
            )
        user_uuid, token = raw_token.split(":", 1)

        cache_key = f"user_token:{user_uuid}"
        stored_token = cache.get(cache_key)

        if stored_token != token:
            return Response(
                {"error": "Token 驗證失敗"}, status=status.HTTP_401_UNAUTHORIZED
            )
        request.user_uuid = user_uuid
        return view_func(self, request, *args, **kwargs)

    return warpper


# FBV驗證裝飾器
def token_required_fbv(view_func):
    @wraps(view_func)
    def warpper(request, *args, **kwargs):
        raw_token = request.COOKIES.get("auth_token")
        if not raw_token or ":" not in raw_token:
            return Response(
                {"error": "未提供 Token"}, status=status.HTTP_401_UNAUTHORIZED
            )
        user_uuid, token = raw_token.split(":", 1)

        cache_key = f"user_token:{user_uuid}"
        stored_token = cache.get(cache_key)

        if stored_token != token:
            return Response(
                {"error": "Token 驗證失敗"}, status=status.HTTP_401_UNAUTHORIZED
            )
        request.user_uuid = user_uuid
        return view_func(request, *args, **kwargs)

    return warpper


def optional_token_cbv(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        raw_token = request.COOKIES.get("auth_token")
        request.user_uuid = None

        if raw_token and ":" in raw_token:
            try:
                user_uuid, token = raw_token.split(":", 1)
                cache_key = f"user_token:{user_uuid}"
                if cache.get(cache_key) == token:
                    request.user_uuid = user_uuid
            except Exception:
                pass

        return view_func(self, request, *args, **kwargs)

    return wrapper


def check_merchant_role(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):

        user = get_object_or_404(User, uuid=request.user_uuid)

        if user.role not in ["merchant", "vip_merchant"]:
            return Response({"error": "您不是商家用戶"}, status=403)

        request.user = user
        return view_func(self, request, *args, **kwargs)

    return wrapper
