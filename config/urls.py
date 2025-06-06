from django.contrib import admin
from django.urls import path, include
from .views import homepage

urlpatterns = [
    path('', homepage),
    path('5th-floor/', admin.site.urls),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/coupons/', include('promotions.coupon_urls')),
    path('api/v1/promotions/', include('promotions.promotion_urls')),
    path('api/v1/restaurants/', include('restaurants.urls')),
    path('api/v1/favorites/', include('users.favorite_urls')),
    path('api/v1/user-coupons/', include('users.user_coupon_urls')),
    path('api/v1/merchants/', include('promotions.merchant_urls')),
    path('api/v1/payments/', include('payments.urls'))
]
