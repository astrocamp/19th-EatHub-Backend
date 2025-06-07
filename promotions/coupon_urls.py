from django.urls import path

from .views import ClaimCouponView, CouponDetailView, CouponUsageView, CreateCouponView

urlpatterns = [
    path('', CreateCouponView.as_view()),
    path('<uuid:uuid>/', CouponDetailView.as_view()),
    path('<uuid:uuid>/claim/', ClaimCouponView.as_view()),
    path('<uuid:uuid>/usage/', CouponUsageView.as_view()),
]
