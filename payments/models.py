import uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone

from users.models import User


# Create your models here.
class Product(models.Model):
    PLAN_CHOICES = [
        ('monthly', 'monthly'),
        ('yearly', 'yearly'),
    ]
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=10, choices=PLAN_CHOICES)
    amount = models.IntegerField()
    interval_days = models.IntegerField()

    def __str__(self):
        return f'{self.name} - {self.get_plan_type_display()}'


class PaymentMethod(models.TextChoices):
    ECPAY = 'ecpay', '綠界'
    LINEPAY = 'linepay', 'LINE Pay'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, default=1)
    start_date = models.DateField(auto_now_add=True)
    ended_at = models.DateField(blank=True, null=True)
    next_payment_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        today = timezone.now().date()
        if not self.ended_at:
            self.ended_at = today + timedelta(days=self.product.interval_days - 1)
            self.next_payment_date = self.ended_at + timedelta(days=1)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.user_name} 訂閱 {self.product}'


class PaymentOrder(models.Model):
    order_id = models.CharField(max_length=50, unique=True, editable=False)
    transaction_id = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_orders')
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payment_orders',
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT, default=1)
    amount = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=20, choices=PaymentMethod.choices)

    def save(self, *args, **kwargs):
        if not self.order_id:
            today = timezone.now().strftime('%Y%m%d')
            random_suffix = uuid.uuid4().hex[:8]
            self.order_id = f'order_{today}_{random_suffix}'
        super().save(*args, **kwargs)

    def __str__(self):
        status = '已付款' if self.is_paid else '未付款'
        return f'{self.order_id} - {status}'


class PaymentLog(models.Model):
    payment_order = models.ForeignKey('PaymentOrder', on_delete=models.CASCADE, related_name='logs')
    request_payload = models.JSONField()
    response_payload = models.JSONField()
    return_code = models.CharField(max_length=10)
    return_message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=20, choices=PaymentMethod.choices)

    def __str__(self):
        return f'Log for Order {self.payment_order.order_id} at {self.created_at}'
