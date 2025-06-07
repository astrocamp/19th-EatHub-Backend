import uuid

from django.db import models


# 使用者(商家使用者)
class User(models.Model):
    email = models.EmailField(unique=True, max_length=254)  # 電子郵件（唯一）
    password = models.CharField(max_length=128)  # 密碼（要先判斷加密）
    user_name = models.CharField(max_length=100)  # 顯示名稱
    first_name = models.CharField(max_length=50, blank=True, null=True)  # 名字，可空
    last_name = models.CharField(max_length=50, blank=True, null=True)  # 姓氏，可空
    image_url = models.URLField(max_length=300, blank=True, null=True)  # 頭像網址，可空
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間，預設為現在
    google_id = models.CharField(max_length=100, blank=True, null=True, unique=True)  # google登入用
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # uuid

    class Role(models.TextChoices):
        MEMBER = 'member', '一般會員'
        MERCHANT = 'merchant', '商家'
        VIP_MERCHANT = 'vip_merchant', 'VIP 商家'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
    )  # 三種角色,預設 一般會員
    # 專屬商家部分
    is_vip = models.BooleanField(default=False)  # 是否為 VIP，預設 False
    license_url = models.URLField(max_length=255, blank=True, null=True)  # 營業證網址，可空
    restaurant = models.ForeignKey(
        'restaurants.Restaurant',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='merchant_user',
    )  # 綁定餐廳，可空

    def __str__(self):
        return self.email  # 方便shell顯示


# 使用者酷碰卷
class UserCoupon(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='claimed_coupons'
    )  # 領取此優惠券的使用者
    coupon = models.ForeignKey(
        'promotions.Coupon', on_delete=models.CASCADE, related_name='claimed_by'
    )  # 對應優惠券
    used_at = models.DateTimeField(blank=True, null=True)  # 使用時間，可空
    is_used = models.BooleanField(default=False)  # 是否已使用，預設 False
    claimed_at = models.DateTimeField(auto_now_add=True)  # 領取時間，預設為現在
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # uuid


# 使用者收藏
class Favorite(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='favorites')  # 收藏者
    restaurant = models.ForeignKey(
        'restaurants.Restaurant', on_delete=models.CASCADE, related_name='favorited_by'
    )  # 被收藏的餐廳
    created_at = models.DateTimeField(auto_now_add=True)  # 收藏時間
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # uuid
