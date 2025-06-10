import os
import uuid

import requests
from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurants.serializers import FullRestaurantSerializer
from utilities.email_util import send_email

from .models import Favorite, User, UserCoupon
from .serializers import (
    LoginSerializer,
    MerchantSignupSerializer,
    SignupSerializer,
    UpdateUserCouponSerializer,
    UserCouponListSerializer,
    UserCouponSerializer,
)
from .utils import check_merchant_role, token_required_cbv


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': '註冊成功',
                    'user': {
                        'uuid': user.uuid,
                        'userName': user.user_name,
                        'email': user.email,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    token = str(uuid.uuid4())
                    cache_key = f'user_token:{user.uuid}'
                    cache.set(cache_key, token, timeout=3600)

                    response = Response(
                        {
                            'user': {
                                'firstName': user.first_name or '',
                                'lastName': user.last_name or '',
                                'userName': user.user_name,
                                'role': user.role,
                                'restaurantUuid': user.restaurant.uuid if user.restaurant else None,
                            },
                            'message': '登入成功',
                        }
                    )

                    cookie_value = f'{user.uuid}:{token}'
                    response.set_cookie(
                        'auth_token',
                        cookie_value,
                        httponly=True,
                        max_age=3600,
                        secure=True,
                        samesite=None,
                    )
                    return response
                else:
                    return Response(
                        {'error': '帳號或是密碼錯誤，請重新輸入。'},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            except User.DoesNotExist:
                return Response(
                    {'error': '帳號或是密碼錯誤，請重新輸入。'},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response({'error': '帳號或是密碼錯誤，請重新輸入。'}, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    @token_required_cbv
    def get(self, request):
        try:
            user = User.objects.get(uuid=request.user_uuid)
            return Response(
                {
                    'message': '驗證成功',
                    'user_uuid': str(user.uuid),
                    'userName': user.user_name,
                    'email': user.email,
                    'role': user.role,
                },
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response({'error': '使用者不存在'}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    def post(self, request):
        raw_token = request.COOKIES.get('auth_token')
        if not raw_token or ':' not in raw_token:
            return Response(
                {'error': '未提供 Token'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_uuid, token = raw_token.split(':', 1)
        cache_key = f'user_token:{user_uuid}'
        cache.delete(cache_key)

        response = Response({'message': '登出成功'})
        response.delete_cookie('auth_token')
        return response


class UserCouponListView(APIView):
    @token_required_cbv
    def get(self, request):
        user_uuid = request.user_uuid  # token_required 驗證後會附上這個屬性
        user_coupons = UserCoupon.objects.filter(user__uuid=user_uuid)

        serializer = UserCouponListSerializer(user_coupons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCouponView(APIView):
    @token_required_cbv
    def get(self, request, uuid):
        user_coupon = get_object_or_404(UserCoupon, uuid=uuid)

        serializer = UserCouponSerializer(user_coupon)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @token_required_cbv
    def delete(self, request, uuid):
        deleted_count, _ = UserCoupon.objects.filter(
            uuid=uuid, user__uuid=request.user_uuid
        ).delete()

        if deleted_count:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)

    @token_required_cbv
    @check_merchant_role
    def patch(self, request, uuid):
        serializer = UpdateUserCouponSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_coupon = UserCoupon.objects.select_related('coupon__restaurant').get(uuid=uuid)
        except UserCoupon.DoesNotExist:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)

        if request.user.restaurant != user_coupon.coupon.restaurant:
            return Response({'success': False}, status=status.HTTP_403_FORBIDDEN)

        try:
            is_used = request.data.get('is_used')
            user_coupon.is_used = is_used
            user_coupon.used_at = timezone.now() if is_used else None
            user_coupon.save()

            return Response(
                {
                    'message': 'success',
                    'coupon': {'serialNumber': user_coupon.coupon.serial_number},
                },
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response({'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FavoriteListView(APIView):
    @token_required_cbv
    def get(self, request):
        user = get_object_or_404(User, uuid=request.user_uuid)
        favorites = (
            Favorite.objects.filter(user=user).select_related('restaurant').order_by('-created_at')
        )
        restaurants = [f.restaurant for f in favorites]

        serializer = FullRestaurantSerializer(restaurants, many=True)
        return Response({'restaurants': serializer.data}, status=status.HTTP_200_OK)


# Google登入
class GoogleLoginView(APIView):
    def post(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': '缺少 access_token'}, status=status.HTTP_400_BAD_REQUEST)

        # 向 Google 拿使用者資訊
        google_user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        google_response = requests.get(google_user_info_url, headers=headers)

        if google_response.status_code != 200:
            return Response(
                {'error': 'Google token 無效或過期'}, status=status.HTTP_400_BAD_REQUEST
            )

        data = google_response.json()
        google_id = data.get('sub')
        email = data.get('email')
        name = data.get('name') or 'Google使用者'

        if not google_id or not email:
            return Response({'error': 'Google 回傳資料不完整'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(
            google_id=google_id,
            defaults={
                'email': email,
                'user_name': name,
            },
        )

        token = str(uuid.uuid4())
        cache.set(f'user_token:{user.uuid}', token, timeout=3600)

        response = Response(
            {
                'message': '登入成功（Google）',
                'user': {
                    'uuid': user.uuid,
                    'userName': user.user_name,
                    'email': user.email,
                },
            }
        )
        response.set_cookie(
            'auth_token',
            f'{user.uuid}:{token}',
            httponly=True,
            secure=True,
            samesite=None,
            max_age=3600,
        )
        return response


class MerchantSignupView(APIView):
    def post(self, request):
        serializer = MerchantSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': '商家註冊成功',
                    'user': {
                        'uuid': user.uuid,
                        'userName': user.user_name,
                        'email': user.email,
                        'role': user.role,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'error': '請提供郵件地址'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)

        # 生成重設密碼的 token
        reset_token = str(uuid.uuid4())

        # 將 token 存入 cache，30 分鐘過期
        cache.set(f'password_reset:{user.uuid}', reset_token, timeout=1800)

        # 構建重設密碼連結
        frontend_domain = os.getenv('FRONTEND_DOMAIN', 'https://eathub.today')
        reset_url = f'{frontend_domain}/reset-password?token={reset_token}&user_id={user.uuid}'

        # 發送郵件
        subject = 'EatHub - 重設密碼'
        html = f"""
        <html>
        <body>
            <h2>重設您的密碼</h2>
            <p>親愛的 {user.user_name}，</p>
            <p>請點擊下方連結重設密碼：</p>
            <p><a href="{reset_url}">重設密碼</a></p>
            <p>連結將在 30 分鐘後失效</p>
        </body>
        </html>
        """

        try:
            send_email(email, subject, html)
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetPasswordView(APIView):
    def post(self, request):
        token = request.data.get('token')
        user_id = request.data.get('user_id')
        new_password = request.data.get('new_password')

        user = User.objects.get(uuid=user_id)

        # 驗證 token
        cache_key = f'password_reset:{user.uuid}'
        stored_token = cache.get(cache_key)

        if stored_token == token:
            # 更新密碼
            user.password = make_password(new_password)
            user.save()

            # 清除 token
            cache.delete(cache_key)

            return Response({'success': True}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
