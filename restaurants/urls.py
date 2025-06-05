from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommendRestaurants),
    path('<uuid:restaurant_uuid>/reviews/', views.create_review),
    path('<uuid:uuid>/favorites/', views.FavoriteRestaurantView.as_view()),
    path('<uuid:uuid>', views.RestaurantDetailView.as_view()),
    path('recent-viewed/', views.RecentViewedRestaurantsView.as_view()),
]
