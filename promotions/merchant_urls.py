from django.urls import path

from .views import MerchantView

urlpatterns = [
    path("me/", MerchantView.as_view()),
]
