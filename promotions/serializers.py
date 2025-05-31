from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Coupon, Promotion
from django.core.files.base import ContentFile
from utilities.cloudinary_upload import upload_to_cloudinary
import uuid

from users.models import UserCoupon

class CouponSerializer(serializers.ModelSerializer):
    restaurant = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        exclude = ['id'] 

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
        exclude = ['id']

MAX_IMAGE_SIZE = 1 * 1024 * 1024  # 1MB

class PromotionsCreateSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(read_only=True)

    class Meta:
        model = Promotion
        fields = ['title', 'description', 'started_at', 'ended_at', 'image_url']
        read_only_fields = ['image_url']

    def create(self, validated_data):
        request = self.context.get('request')
        restaurant = self.context.get('restaurant')

        image_file = request.FILES.get('image')
        if image_file:
            try:
                image_data = image_file.read()
                if len(image_data) > MAX_IMAGE_SIZE:
                    raise ValueError('圖片太大，請小於 1MB')

                filename = f'promotion_{uuid.uuid4()}.jpg'
                image_url = upload_to_cloudinary(ContentFile(image_data, name=filename), filename)

                validated_data['image_url'] = image_url
            except Exception as e:
                raise serializers.ValidationError({'image': f'圖片處理失敗：{str(e)}'})

        return Promotion.objects.create(
            restaurant=restaurant,
            **validated_data
        )
class MerchantCouponSerializer(CouponSerializer):
    redeemed_count = serializers.SerializerMethodField()
    used_count = serializers.SerializerMethodField()

    def get_redeemed_count(self, obj):
        return obj.claimed_by.count()

    def get_used_count(self, obj):
        return obj.claimed_by.filter(is_used=True).count()
class UserCouponUsageSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email')

    class Meta:
        model = UserCoupon
        fields = ['uuid', 'user', 'is_used']
