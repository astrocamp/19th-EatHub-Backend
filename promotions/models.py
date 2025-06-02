import uuid

from django.db import models


# 最新消息
class Promotion(models.Model):
    title = models.CharField(max_length=255)  # 活動標題
    description = models.TextField(blank=True, null=True)  # 活動描述，可空
    started_at = models.DateTimeField(blank=True, null=True)  # 開始時間，可空
    ended_at = models.DateTimeField(blank=True, null=True)  # 結束時間，可空
    is_archived = models.BooleanField(default=False)  # 是否封存，預設 False
    image_url = models.URLField(
        max_length=255, blank=True, null=True
    )  # 活動圖片網址，可空
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="promotions",
    )  # 所屬餐廳
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # uuid


# 酷碰卷
class Coupon(models.Model):
    serial_number = models.CharField(max_length=255, unique=True)  # 優惠券序號（唯一）
    ended_at = models.DateTimeField(blank=True, null=True)  # 到期時間，可空
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="coupons",
    )  # 所屬餐廳
    title = models.CharField(max_length=255)  # 優惠券標題
    description = models.TextField(blank=True, null=True)  # 說明文字，可空
    discount_type = models.CharField(max_length=255)  # 折扣類型（例：金額、百分比）
    discount_value = models.PositiveIntegerField(blank=True, null=True)  # 折扣值，可空
    total = models.PositiveIntegerField(blank=True, null=True)  # 發行總數，可空
    is_archived = models.BooleanField(default=False)  # 是否封存，預設 False
    started_at = models.DateTimeField(blank=True, null=True)  # 開始時間，可空
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # uuid

    def __str__(self):
        return f"{self.title} - {self.restaurant.name}"
