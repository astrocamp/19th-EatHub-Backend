from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import datetime

@api_view(['GET'])
def health_check(request):
    
    from django.http import HttpResponse

    return HttpResponse("HTTP 200 OK", content_type="text/plain")

@api_view(['GET'])
def detailed_health_check(request):
   
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()  
            db_status = "connected"
    except Exception as e:
     
        db_status = f"error: {str(e)}"
    
    overall_status = "healthy" if db_status == "connected" else "degraded"
    
    response_status = status.HTTP_200_OK if overall_status == "healthy" else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return Response({
        'status': overall_status,
        'timestamp': datetime.datetime.now().isoformat(),
        'checks': {
            'database': db_status,
        },
        'system_info': {
            'django_version': '4.2.20',
            'environment': 'development' if __debug__ else 'production',
            'debug_mode': __debug__
        }
    }, status=response_status)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', health_check, name='health_check'),
    path('health/', detailed_health_check, name='detailed_health'),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/coupons/', include('promotions.coupon_urls')),
    path('api/v1/promotions/', include('promotions.promotion_urls')),
    path('api/v1/restaurants/', include('restaurants.urls')),
    path('api/v1/favorites/', include('users.favorite_urls')),
    path('api/v1/user-coupons/', include('users.user_coupon_urls')),
    path('api/v1/merchants/', include('promotions.merchant_urls')),
    path('api/v1/payments/', include('payments.urls')),
]