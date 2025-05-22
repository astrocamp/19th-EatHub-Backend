from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.core.cache import cache
from users.models import User

class CustomCookieAuthentication(BaseAuthentication):
    def authenticate(self, request):
        cookie = request.COOKIES.get('auth_token')
        if not cookie:
            return None

        try:
            uuid_str, token = cookie.split(':')
        except ValueError:
            raise AuthenticationFailed('Invalid cookie format')

        cache_key = f'user_token:{uuid_str}'
        cached_token = cache.get(cache_key)

        if cached_token != token:
            raise AuthenticationFailed('Invalid or expired token')

        try:
            user = User.objects.get(uuid=uuid_str)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, None)
