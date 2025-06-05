from rest_framework import serializers
from payments.models import Product,PaymentOrder

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['uuid', 'name', 'plan_type', 'amount', 'interval_days']

class PaymentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOrder
        fields = ['order_id', 'amount', 'is_paid', 'transaction_id', 'created_at']