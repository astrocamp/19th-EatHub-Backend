from django.urls import path
from .views import PromotionDetailView, PromotionCreateView

urlpatterns = [
    path('', PromotionCreateView.as_view()),
    path('<uuid:uuid>/', PromotionDetailView.as_view()),
]
