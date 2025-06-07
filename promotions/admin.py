from django.contrib import admin

from .models import Coupon, Promotion


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('title', 'serial_number', 'restaurant', 'started_at', 'ended_at', 'is_archived')
    autocomplete_fields = ['restaurant']
    search_fields = ('title', 'restaurant__name')
    readonly_fields = ('uuid',)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'restaurant', 'started_at', 'ended_at', 'is_archived')
    search_fields = ('title', 'restaurant__name')
    list_filter = ('is_archived',)
    ordering = ('-started_at',)
    autocomplete_fields = ['restaurant']
    readonly_fields = ('uuid',)
