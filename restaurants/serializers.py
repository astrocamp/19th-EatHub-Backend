from rest_framework import serializers
from .models import Restaurant, Review
from users.serializers import SimpleUserSerializer
from promotions.serializers import PromotionSerializer, CouponSerializer
from utilities.cloudinary_upload import upload_to_cloudinary
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField
import uuid
from django.db.models import Q, Count

MAX_IMAGE_SIZE = 1 * 1024 * 1024
class ReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    image_url = serializers.URLField(read_only=True)

    class Meta:
        model = Review
        fields = ['uuid', 'user', 'restaurant', 'rating', 'content', 'created_at', 'image_url']
        read_only_fields = ['uuid', 'created_at', 'user', 'restaurant', 'image_url']

    def create(self, validated_data):
        user = self.context['user']
        restaurant = self.context['restaurant']
        request = self.context.get('request')

        if Review.objects.filter(user=user, restaurant=restaurant).exists():
            raise serializers.ValidationError({'detail':'該餐廳已評論過。'})
        
        image_file = request.FILES.get('image')
        if image_file:
            try:   
                image_data = image_file.read()           
                if len(image_data) > MAX_IMAGE_SIZE:
                    raise ValueError('圖片太大，請小於 1MB')
                
                filename = f'review_{uuid.uuid4()}.jpg'
                image_url = upload_to_cloudinary(ContentFile(image_data, name=filename), filename)
                validated_data['image_url'] = image_url
            except Exception as e:
                raise serializers.ValidationError({'image_bytes': f'圖片處理失敗: {str(e)}'})
            
        return Review.objects.create(user=user, restaurant=restaurant, **validated_data)

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        exclude = ['id', 'created_at']

class SimpleReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = Review
        fields = ["user", "rating", "content", "created_at", "image_url"]

class SimpleRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name','image_url']

class RestaurantDetailSerializer(serializers.Serializer):
    restaurant = serializers.SerializerMethodField()
    promotion = serializers.SerializerMethodField()
    coupon = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    user_status = serializers.SerializerMethodField()

    def get_restaurant(self, obj):
        return RestaurantSerializer(obj).data
    
    def get_promotion(self, obj):
        now = timezone.now()
        promotions = obj.promotions.filter(
            is_archived=False,
            ended_at__gte=now
        ).order_by("-created_at",)
        return (
            PromotionSerializer(promotions, many=True).data
            if promotions.exists()
            else None
        )
    
    def get_coupon(self, obj):
        now = timezone.now()
        coupons = obj.coupons.filter(
            is_archived=False,
            ended_at__gte=now
        ).order_by("-started_at")
        self._coupons = coupons
        return CouponSerializer(coupons, many=True).data if coupons.exists() else None

    def get_reviews(self, obj):
        reviews = obj.reviews.select_related("user")
        request = self.context.get('request')
        user_uuid = getattr(request, 'user_uuid', None)

        if user_uuid:
            reviews = reviews.annotate(
                priority=Case(
                    When(user__uuid=user_uuid, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField()
                )
            ).order_by('priority', 'created_at')
        return (
            SimpleReviewSerializer(reviews, many=True).data
            if reviews.exists()
            else None
        )
    
    def get_user_status(self, obj):
        request = self.context.get('request')
        user_uuid = getattr(request, 'user_uuid', None)
        coupons = getattr(self, '_coupons', [])
        result = {
            'hasFavorited': False,
            'hasClaimedCoupon': {str(coupon.uuid): False for coupon in coupons},
            'hasReviewed': False
        }

        if not user_uuid:
            return result

        result['hasFavorited'] = obj.favorited_by.filter(user__uuid=user_uuid).exists()
        result['hasReviewed'] = obj.reviews.filter(user__uuid=user_uuid).exists()
        
        for coupon in coupons:
            if coupon:
                result['hasClaimedCoupon'][str(coupon.uuid)] = coupon.claimed_by.filter(user__uuid=user_uuid).exists()

        return result
    
class FullRestaurantSerializer(serializers.ModelSerializer):
     hasAvailableCoupon = serializers.SerializerMethodField()
     class Meta:
        model = Restaurant
        exclude = ['id', 'created_at'] 
        
     def get_hasAvailableCoupon(self, obj):
                now = timezone.now()
                coupons = obj.coupons.filter(
                    is_archived=False,
                ).filter(
                    Q(started_at__lte=now) | Q(started_at__isnull=True),
                    Q(ended_at__gte=now) | Q(ended_at__isnull=True),
                ).annotate(
                    claimed_count=Count('claimed_by')
                )
                return any(
                    coupon.total is None or coupon.claimed_count < coupon.total
                    for coupon in coupons
                )