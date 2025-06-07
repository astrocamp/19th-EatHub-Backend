from django.urls import path

from .views import FavoriteListView

urlpatterns = [
    path('', FavoriteListView.as_view()),
]
