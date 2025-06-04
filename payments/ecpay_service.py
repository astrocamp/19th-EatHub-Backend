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
        order_id = self.payment_order.order_id[:20]
        total_amount = self.payment_order.amount

        merchant_trade_no = ''.join(filter(str.isalnum, order_id))[:20].upper()

        request_data = {
            'MerchantTradeNo': merchant_trade_no,
            'MerchantTradeDate': trade_date,
            'TotalAmount': total_amount,
            'TradeDesc': quote_plus("EatHub VIP 訂閱"),
            'ItemName': f"{self.product.name} x 1",
            'ReturnURL': settings.ECPAY_RETURN_URL,
            'ClientBackURL': settings.ECPAY_CLIENT_BACK_URL,
            'ChoosePayment': ChoosePayment['ALL'],
            'NeedExtraPaidInfo': 'N',
            'EncryptType': 1,
        }

        # 回傳 HTML <form> 字串，前端可以直接渲染使用
        params = self.sdk.create_order(request_data)
        form_html = self.sdk.gen_html_post_form(settings.ECPAY_GATEWAY_URL, params)

        return {
            'order_id': self.payment_order.order_id,
            'form_html': form_html
        }