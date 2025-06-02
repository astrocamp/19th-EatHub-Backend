from django.urls import path

from .views import UserCouponDeleteView, UserCouponListView

urlpatterns = [
    path("", UserCouponListView.as_view()),
    path("<uuid:uuid>/", UserCouponDeleteView.as_view()),
]
