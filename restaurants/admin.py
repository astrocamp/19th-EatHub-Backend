from django.contrib import admin

from .models import Restaurant, Review


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone", "google_rating", "place_id")
    search_fields = ("name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "restaurant", "rating", "created_at")
    search_fields = ("user__email", "restaurant__name", "content")
    list_filter = ("rating",)
    ordering = ("-created_at",)
    autocomplete_fields = ["restaurant", "user"]
