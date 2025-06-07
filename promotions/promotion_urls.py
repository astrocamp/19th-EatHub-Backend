from django.urls import path

from .views import PromotionCreateView, PromotionDetailView

urlpatterns = [
    path('', PromotionCreateView.as_view()),
    path('<uuid:uuid>/', PromotionDetailView.as_view()),
]
