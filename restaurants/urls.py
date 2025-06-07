from django.urls import path

from . import views

urlpatterns = [
    path('', views.RecommendRestaurants.as_view()),
    path('<uuid:restaurant_uuid>/reviews/', views.CreateReview.as_view()),
    path('<uuid:uuid>/favorites/', views.FavoriteRestaurantView.as_view()),
    path('<uuid:uuid>', views.RestaurantDetailView.as_view()),
    path('recent-viewed/', views.RecentViewedRestaurantsView.as_view()),
]
