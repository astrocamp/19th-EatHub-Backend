from utilities.ecpay_payment_sdk import ECPayPaymentSdk, ChoosePayment
from django.conf import settings
from datetime import datetime
from urllib.parse import quote_plus

class ECPayService:
    def __init__(self, payment_order, product):
        self.payment_order = payment_order
        self.product = product
        self.sdk = ECPayPaymentSdk(
            MerchantID=settings.ECPAY_MERCHANT_ID,
            HashKey=settings.ECPAY_HASH_KEY,
            HashIV=settings.ECPAY_HASH_IV,
        )

    def send_payment_request(self):
        trade_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        order_id = self.payment_order.order_id
        total_amount = self.payment_order.amount

        request_data = {
            'MerchantTradeNo': order_id[:20],  # ECPay 限制最多 20 字
            'MerchantTradeDate': trade_date,
            'TotalAmount': total_amount,
            'TradeDesc': quote_plus("EatHub VIP 訂閱"),
            'ItemName': f"{self.product.name} x 1",
            'ReturnURL': settings.ECPAY_RETURN_URL,  # 伺服器回傳
            'ClientBackURL': settings.ECPAY_CLIENT_BACK_URL,  # 用戶返回
            'ChoosePayment': ChoosePayment['ALL'],
            'NeedExtraPaidInfo': 'N',
        }

        form_html = self.sdk.create_order(request_data)

        return {
            'order_id': order_id,
            'payment_url_web': settings.ECPAY_GATEWAY_URL,
            'form_html': form_html  # 給前端渲染跳轉
        }
