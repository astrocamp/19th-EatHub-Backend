from rest_framework import serializers

from payments.models import PaymentOrder, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['uuid', 'name', 'plan_type', 'amount', 'interval_days']


class PaymentOrderSerializer(serializers.ModelSerializer):
    vip_expiry = serializers.DateField(source='subscription.ended_at', read_only=True)

    class Meta:
        model = PaymentOrder
        fields = ['order_id', 'amount', 'is_paid', 'transaction_id', 'created_at', 'vip_expiry']
