from rest_framework.exceptions import ValidationError

from payments.models import Product


def validate_payment_request(data):
    product_id = data.get('product_id')
    amount_input = data.get('amount')

    if not product_id or not amount_input:
        raise ValidationError('缺少參數')

    try:
        amount = int(amount_input)
    except ValueError:
        raise ValidationError('金額需為整數')

    try:
        product = Product.objects.get(uuid=product_id)
    except Product.DoesNotExist:
        raise ValidationError('找不到產品')

    if product.amount != amount:
        raise ValidationError('金額不正確')

    return product, amount
