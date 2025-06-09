from datetime import timedelta

from django.utils import timezone

from payments.models import Subscription
from users.models import User


def create_subscription_after_payment(user, product):
    # 付款成功後建立訂閱，並升級商家為 VIP
    today = timezone.now().date()
    latest_sub = Subscription.objects.filter(user=user).order_by('-ended_at').first()

    if latest_sub and latest_sub.ended_at and latest_sub.ended_at >= today:
        start_date = latest_sub.ended_at + timedelta(days=1)
    else:
        start_date = today

    ended_at = start_date + timedelta(days=product.interval_days - 1)
    next_payment_date = ended_at - timedelta(days=7)
    subscription = Subscription.objects.create(
        user=user,
        product=product,
        start_date=start_date,
        ended_at=ended_at,
        next_payment_date=next_payment_date,
    )
    if user.role == User.Role.MERCHANT:
        user.role = User.Role.VIP_MERCHANT
        user.is_vip = True
        user.save()
    return subscription
