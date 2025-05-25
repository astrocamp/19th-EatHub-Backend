from rest_framework import viewsets, status
from .models import Coupon
from .serializers import CouponSerializer
from rest_framework.views import APIView
from users.utils import token_required_cbv  
from django.shortcuts import get_object_or_404
from users.models import User, UserCoupon
from rest_framework.response import Response

class CreateCouponView(APIView):
    @token_required_cbv
    def post(self, request):
        user = User.objects.filter(uuid=request.user_uuid).first()
        if not user:
            return Response({'error': '使用者未登入或不存在'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.role not in ['merchant', 'vip_merchant']:
            return Response({'error': '僅限商家使用者新增優惠券'}, status=status.HTTP_403_FORBIDDEN)

        if user.role == 'merchant':
            has_coupon = Coupon.objects.filter(restaurant=user.restaurant, is_archived=False).exists()
            if has_coupon:
                return Response({'error': '一般商家僅能擁有一張有效優惠券'}, status=status.HTTP_403_FORBIDDEN)
        if user.role == 'vip_merchant':
            count = Coupon.objects.filter(restaurant=user.restaurant, is_archived=False).count()
            if count >= 3:
                return Response({'error': 'VIP 商家最多只能擁有三張有效優惠券'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data.copy()
        serializer = CouponSerializer(data=data)

        if serializer.is_valid():
            serializer.save(restaurant=user.restaurant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClaimCouponView(APIView):
    @token_required_cbv
    def post(self, request, uuid):
        user = get_object_or_404(User, uuid=request.user_uuid)
        coupon = get_object_or_404(Coupon, uuid=uuid, is_archived=False)

        if UserCoupon.objects.filter(user=user, coupon=coupon).exists():
            return Response({'success': False}, status=status.HTTP_200_OK)
        
        UserCoupon.objects.create(user=user, coupon=coupon)
        return Response({'success': True}, status=status.HTTP_201_CREATED)
