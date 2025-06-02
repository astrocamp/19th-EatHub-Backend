from django.urls import path

from .views import PromotionDetailView

urlpatterns = [
    path("<uuid:uuid>/", PromotionDetailView.as_view()),
]
