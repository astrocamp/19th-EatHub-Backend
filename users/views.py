from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.core.cache import cache
import uuid
from .models import User,UserCoupon,Favorite
from .serializers import SignupSerializer, LoginSerializer, UserCouponListSerializer
from .utils import token_required_cbv
from django.shortcuts import get_object_or_404
import requests
from restaurants.serializers import RestaurantSerializer

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
                    cache.set(cache_key, token, timeout=36000)

                    response = Response(
                        {
                            'user': {
                                'firstName': user.first_name,
                                'lastName': user.last_name,
                                'userName': user.user_name,
                            },
                            'message': '登入成功',
                        }
                    )

                    cookie_value = f'{user.uuid}:{token}'
                    response.set_cookie(
                        'auth_token',
                        cookie_value,
                        httponly=True,
                        max_age=36000,
                        secure=True,
                        samesite='lax',
                    )
                    return response
                else:
                    return Response(
                        {'error': '密碼錯誤'},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            except User.DoesNotExist:
                return Response(
                    {'error': '使用者不存在'},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    @token_required_cbv
    def get(self, request):
        try:
            user = User.objects.get(uuid=request.user_uuid)
            return Response({
                'message': '驗證成功',
                'user_uuid': str(user.uuid),
                'userName': user.user_name,
                'email': user.email,
            }, status=status.HTTP_200_OK)
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

class UserCouponDeleteView(APIView):
    @token_required_cbv
    def delete(self, request, uuid):
        deleted_count, _ = UserCoupon.objects.filter(
            uuid=uuid,
            user__uuid=request.user_uuid
        ).delete()

        if deleted_count:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': '找不到這張優惠券或無權限刪除'}, status=status.HTTP_404_NOT_FOUND)

class FavoriteListView(APIView):
    @token_required_cbv
    def get(self, request):
        user = get_object_or_404(User, uuid=request.user_uuid)
        favorites = Favorite.objects.filter(user=user).select_related('restaurant').order_by('-created_at')
        restaurants = [f.restaurant for f in favorites]

        serializer = RestaurantSerializer(restaurants, many=True)
        return Response({"restaurants": serializer.data}, status=status.HTTP_200_OK)

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
            return Response({'error': 'Google token 無效或過期'}, status=status.HTTP_400_BAD_REQUEST)

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
            }
        )

        token = str(uuid.uuid4())
        cache.set(f'user_token:{user.uuid}', token, timeout=3600)

        response = Response({
            'message': '登入成功（Google）',
            'user': {
                'uuid': user.uuid,
                'userName': user.user_name,
                'email': user.email,
            }
        })
        response.set_cookie(
            'auth_token',
            f'{user.uuid}:{token}',
            httponly=True,
            secure=False,     # 本地使用 False，上線請改 True
            samesite='Lax',
            max_age=3600,
        )
        return response
        