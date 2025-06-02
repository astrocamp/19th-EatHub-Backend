from django.contrib import admin

from users.models import Favorite, User, UserCoupon


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "user_name", "role", "is_vip", "created_at")
    list_filter = ("role", "is_vip")
    search_fields = ("email", "user_name")
    ordering = ("-created_at",)
    autocomplete_fields = ["restaurant"]


@admin.register(UserCoupon)
class UserCouponAdmin(admin.ModelAdmin):
    list_display = ("uuid", "user", "coupon", "is_used", "claimed_at", "used_at")
    list_filter = ("is_used",)
    search_fields = ("user__email", "coupon__title")
    ordering = ("-claimed_at",)
    autocomplete_fields = ["user", "coupon"]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("uuid", "user", "restaurant", "created_at")
    search_fields = ("user__email", "restaurant__name")
    ordering = ("-created_at",)
    autocomplete_fields = ["restaurant", "user"]
