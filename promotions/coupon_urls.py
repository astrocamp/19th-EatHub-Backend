from django.urls import path
from .views import CreateCouponView, ClaimCouponView

urlpatterns = [
    path('', CreateCouponView.as_view()),
    path('<uuid:uuid>/claim/', ClaimCouponView.as_view())
]