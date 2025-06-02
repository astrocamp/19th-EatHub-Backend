from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, UserCoupon
from users.utils import check_merchant_role, token_required_cbv

from .models import Coupon, Promotion
from .serializers import (
    CouponSerializer,
    MerchantCouponSerializer,
    PromotionSerializer,
    UserCouponUsageSerializer,
)


class CreateCouponView(APIView):
    @token_required_cbv
    def post(self, request):
        user = User.objects.filter(uuid=request.user_uuid).first()
        if not user:
            return Response(
                {"error": "使用者未登入或不存在"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if user.role not in ["merchant", "vip_merchant"]:
            return Response(
                {"error": "僅限商家使用者新增優惠券"}, status=status.HTTP_403_FORBIDDEN
            )

        if user.role == "merchant":
            has_coupon = Coupon.objects.filter(
                restaurant=user.restaurant, is_archived=False
            ).exists()
            if has_coupon:
                return Response(
                    {"error": "一般商家僅能擁有一張有效優惠券"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        if user.role == "vip_merchant":
            count = Coupon.objects.filter(
                restaurant=user.restaurant, is_archived=False
            ).count()
            if count >= 3:
                return Response(
                    {"error": "VIP 商家最多只能擁有三張有效優惠券"},
                    status=status.HTTP_403_FORBIDDEN,
                )
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
            return Response({"success": False}, status=status.HTTP_200_OK)

        UserCoupon.objects.create(user=user, coupon=coupon)
        return Response({"success": True}, status=status.HTTP_201_CREATED)


class MerchantView(APIView):
    @token_required_cbv
    def get(self, request):
        user = get_object_or_404(User, uuid=request.user_uuid)
        if user.role not in ["merchant", "vip_merchant"]:
            return Response(
                {"error": "目前非商家帳號，請先建立店家"},
                status=status.HTTP_403_FORBIDDEN,
            )

        restaurant = user.restaurant
        if not restaurant:
            return Response(
                {"error": "此商家尚未綁定餐廳"}, status=status.HTTP_400_BAD_REQUEST
            )

        promotions = Promotion.objects.filter(restaurant=restaurant, is_archived=False)
        coupons = Coupon.objects.filter(restaurant=restaurant, is_archived=False)

        return Response(
            {
                "result": {
                    "restaurant": {
                        "uuid": str(restaurant.uuid),
                        "name": restaurant.name,
                    },
                    "promotions": PromotionSerializer(promotions, many=True).data,
                    "coupons": MerchantCouponSerializer(coupons, many=True).data,
                }
            }
        )


class CouponUsageView(APIView):
    @token_required_cbv
    def get(self, request, uuid):
        user = get_object_or_404(User, uuid=request.user_uuid)
        coupon = get_object_or_404(Coupon, uuid=uuid)

        if user.restaurant != coupon.restaurant:
            return Response({"success": False, "message": "無觀看權限"}, status=403)

        user_coupons = UserCoupon.objects.filter(coupon=coupon).select_related("user")
        serializer = UserCouponUsageSerializer(user_coupons, many=True)

        return Response(
            {"title": coupon.title, "usages": serializer.data},
            status=status.HTTP_200_OK,
        )


class CouponDetailView(APIView):
    @token_required_cbv
    @check_merchant_role
    def get(self, request, uuid):
        user = get_object_or_404(User, uuid=request.user_uuid)

        coupon = get_object_or_404(Coupon, uuid=uuid, is_archived=False)
        if user.restaurant != coupon.restaurant:
            return Response(
                {"error": "您無權限查看此最新動態"}, status=status.HTTP_403_FORBIDDEN
            )
        serializer = CouponSerializer(coupon)
        result = serializer.data
        result["total_claimed"] = UserCoupon.objects.filter(coupon=coupon).count()
        result["total_used"] = UserCoupon.objects.filter(
            coupon=coupon, is_used=True
        ).count()

        return Response({"result": result}, status=status.HTTP_200_OK)

    @token_required_cbv
    def patch(self, request, uuid):
        user = get_object_or_404(User, uuid=request.user_uuid)

        if user.role not in ["merchant", "vip_merchant"]:
            return Response(
                {"error": "目前非商家帳號"}, status=status.HTTP_403_FORBIDDEN
            )

        restaurant = user.restaurant
        if not restaurant:
            return Response(
                {"error": "此商家尚未綁定餐廳"}, status=status.HTTP_400_BAD_REQUEST
            )

        coupon = get_object_or_404(Coupon, uuid=uuid, restaurant=restaurant)

        coupon.is_archived = True
        coupon.save()

        return Response({"success": True}, status=status.HTTP_200_OK)


class PromotionDetailView(APIView):
    @token_required_cbv
    def get(self, request, uuid):
        user = get_object_or_404(User, uuid=request.user_uuid)

        promotion = get_object_or_404(Promotion, uuid=uuid, is_archived=False)
        if user.restaurant != promotion.restaurant:
            return Response(
                {"error": "您無權限查看此最新動態"}, status=status.HTTP_403_FORBIDDEN
            )
        serializer = PromotionSerializer(promotion)
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)

    @token_required_cbv
    def patch(self, request, uuid):
        user = get_object_or_404(User, uuid=request.user_uuid)

        if user.role not in ["merchant", "vip_merchant"]:
            return Response(
                {"error": "目前非商家帳號"}, status=status.HTTP_403_FORBIDDEN
            )

        restaurant = user.restaurant
        if not restaurant:
            return Response(
                {"error": "此商家尚未綁定餐廳"}, status=status.HTTP_400_BAD_REQUEST
            )

        promotion = get_object_or_404(Promotion, uuid=uuid, restaurant=restaurant)

        promotion.is_archived = True
        promotion.save()

        return Response({"success": True}, status=status.HTTP_200_OK)
