from django.urls import path

from .views import UserCouponListView, UserCouponView

urlpatterns = [
    path('', UserCouponListView.as_view()),
    path('<uuid:uuid>/', UserCouponView.as_view()),
]
