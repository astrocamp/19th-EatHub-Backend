from django.urls import path

from . import views

urlpatterns = [path('', views.PromotionCreateView.as_view())]
