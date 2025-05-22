from rest_framework import serializers
from .models import Restaurant, Review
from users.serializers import SimpleUserSerializer
from promotions.serializers import PromotionSerializer, CouponSerializer

class FullRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    image_url = serializers.URLField(source='img_url', required=False)

    class Meta:
        model = Review
        fields = ['uuid', 'user', 'restaurant', 'rating', 'content', 'created_at', 'image_url']
        read_only_fields = ['uuid', 'created_at', 'user', 'restaurant']
    def create(self, validated_data):
        user = self.context['user']
        restaurant = self.context['restaurant']

        if Review.objects.filter(user=user, restaurant=restaurant).exists():
            raise serializers.ValidationError('該餐廳已評論過。')
        return Review.objects.create(user=user, restaurant=restaurant, **validated_data)

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        exclude = ['id', 'created_at']

class SimpleReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = Review
        fields = ["user", "rating", "content", "created_at", "img_url"]

class SimpleRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name','image_url']

class RestaurantDetailSerializer(serializers.Serializer):
    restaurant = RestaurantSerializer()
    promotion = serializers.SerializerMethodField()
    coupon = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    user_status = serializers.SerializerMethodField()


    def to_representation(self, obj):
        restaurant_data = RestaurantSerializer(obj, context=self.context).data
        return {
            "restaurant": restaurant_data,
            "promotion": self.get_promotion(obj),
            "coupon": self.get_coupon(obj),
            "reviews": self.get_reviews(obj),
            "user_status": self.get_user_status(obj),
        }
    
    def get_promotion(self, obj):
        promotions = obj.promotions.filter(is_archived=False).order_by("-created_at")
        return (
            PromotionSerializer(promotions, many=True).data
            if promotions.exists()
            else None
        )
    
    def get_coupon(self, obj):
        coupon = obj.coupons.filter(is_archived=False).order_by("-started_at").first()
        return CouponSerializer(coupon).data if coupon else None

    def get_reviews(self, obj):
        reviews = obj.reviews.select_related("user").all()
        return (
            SimpleReviewSerializer(reviews, many=True).data
            if reviews.exists()
            else None
        )
    
    def get_user_status(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        result = {
            'hasFavorited': False,
            'hasClaimedCoupon': False,
            'hasReviewed': False
        }

        if not user:
            return result

        result['hasFavorited'] = obj.favorited_by.filter(user=user).exists()
        result['hasReviewed'] = obj.reviews.filter(user=user).exists()

        coupon = getattr(self, '_coupon', None)
        if coupon:
            result['hasClaimedCoupon'] = coupon.claimed_by.filter(user=user).exists()

        return result