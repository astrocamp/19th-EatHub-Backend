import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# 餐廳
class Restaurant(models.Model):
    name = models.CharField(max_length=255)  # 餐廳名稱
    address = models.CharField(max_length=255)  # 地址
    latitude = models.FloatField()  # 緯度
    longitude = models.FloatField()  # 經度
    phone = models.CharField(max_length=255, blank=True, null=True)  # 電話，可空
    open_hours = models.JSONField(blank=True, null=True)  # 營業時間，可空
    google_rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        blank=True,
        null=True,
    )  # Google 評分
    place_id = models.CharField(max_length=100, unique=True)  # Google Place ID
    image_url = models.URLField(max_length=255, blank=True, null=True)  # 店家圖片，可空
    website = models.URLField(max_length=255, blank=True, null=True)  # 官網，可空
    user_ratings_total = models.IntegerField(blank=True, null=True)  # 評價數量，可空
    google_photo_reference = models.TextField(blank=True, null=True)  # Google 照片參考 ID，可空
    types = models.TextField(blank=True, null=True)  # 類型分類，可空
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # uuid

    def __str__(self):
        return self.name


# 評論
class Review(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='reviews',
    )  # 評論者
    restaurant = models.ForeignKey(
        'Restaurant',
        on_delete=models.CASCADE,
        related_name='reviews',
    )  # 被評論餐廳
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=True,
        null=True,
    )  # 評分，可空
    content = models.TextField()  # 評論內容
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    image_url = models.URLField(max_length=255, blank=True, null=True)  # 附圖，可空
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # uuid
