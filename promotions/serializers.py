from rest_framework import serializers

from users.models import UserCoupon

from .models import Coupon, Promotion


class CouponSerializer(serializers.ModelSerializer):
    restaurant = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        exclude = ["id"]

    def get_discount(self, obj):
        if not obj.discount_type or obj.discount_value is None:
            return None

        if obj.discount_type == "金額":
            return f"{obj.discount_value}元 折價券"
        elif obj.discount_type == "百分比":
            discount_rate = round(10 - obj.discount_value / 10, 1)
            return f"{discount_rate}折 折價券"
        else:
            return "未知折扣類型"

    def get_restaurant(self, obj):
        from restaurants.serializers import SimpleRestaurantSerializer

        return SimpleRestaurantSerializer(obj.restaurant).data


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        exclude = ["id"]


class MerchantCouponSerializer(CouponSerializer):
    redeemed_count = serializers.SerializerMethodField()
    used_count = serializers.SerializerMethodField()

    def get_redeemed_count(self, obj):
        return obj.claimed_by.count()

    def get_used_count(self, obj):
        return obj.claimed_by.filter(is_used=True).count()


class UserCouponUsageSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source="user.email")

    class Meta:
        model = UserCoupon
        fields = ["uuid", "user", "is_used"]
