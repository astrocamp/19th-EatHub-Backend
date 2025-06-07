import base64
import hashlib
import hmac
import json
import uuid

import requests
from django.conf import settings

from payments.models import PaymentLog, PaymentMethod


class LinePayService:
    def __init__(self, payment_order, product):
        self.payment_order = payment_order
        self.product = product
        self.amount = payment_order.amount
        self.api_base = settings.LINEPAY_API_BASE_URL
        self.secret = settings.LINEPAY_CHANNEL_SECRET
        self.channel_id = settings.LINEPAY_CHANNEL_ID
        self.domain = settings.PUBLIC_DOMAIN

    # 組裝 LINE PAY 請求資料
    def build_request_payload(self):
        return {
            'amount': self.amount,
            'currency': 'TWD',
            'orderId': self.payment_order.order_id,
            'packages': [
                {
                    'id': str(uuid.uuid4()),
                    'amount': self.amount,
                    'name': self.product.plan_type,
                    'products': [
                        {'name': self.product.plan_type, 'quantity': 1, 'price': self.amount}
                    ],
                }
            ],
            'redirectUrls': {
                'confirmUrl': f'{self.domain}/api/v1/payments/linepay/confirm/',
                'cancelUrl': f'{self.domain}/payment-cancel',
            },
        }

    # 產生簽章
    def generate_signature(self, body: dict, api_path: str):
        nonce = uuid.uuid4().hex
        body_str = json.dumps(body)
        message = self.secret + api_path + body_str + nonce
        signature = base64.b64encode(
            hmac.new(self.secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
        ).decode('utf-8')
        return signature, nonce

    def send_payment_request(self):
        api_path = '/v3/payments/request'
        body = self.build_request_payload()
        signature, nonce = self.generate_signature(body, api_path)

        headers = {
            'Content-Type': 'application/json',
            'X-LINE-ChannelId': self.channel_id,
            'X-LINE-Authorization-Nonce': nonce,
            'X-LINE-Authorization': signature,
        }
        # 發送付款請求
        try:
            res = requests.post(f'{self.api_base}{api_path}', headers=headers, json=body)
            data = res.json()
        except Exception as e:
            PaymentLog.objects.create(
                payment_order=self.payment_order,
                request_payload=body,
                response_payload={'error': str(e)},
                return_code='EXCEPTION',
                return_message='Request failed',
                method=PaymentMethod.LINEPAY,
            )
            raise e

        PaymentLog.objects.create(
            payment_order=self.payment_order,
            request_payload=body,
            response_payload=data,
            return_code=data.get('returnCode', 'N/A'),
            return_message=data.get('returnMessage', 'N/A'),
            method=PaymentMethod.LINEPAY,
        )
        return data

    # LINE PAY 付款確認
    def confirm_payment(self, transaction_id: str):
        api_path = f'/v3/payments/{transaction_id}/confirm/'
        body = {'amount': self.amount, 'currency': 'TWD'}
        signature, nonce = self.generate_signature(body, api_path)
        headers = {
            'Content-Type': 'application/json',
            'X-LINE-ChannelId': self.channel_id,
            'X-LINE-Authorization-Nonce': nonce,
            'X-LINE-Authorization': signature,
        }

        try:
            res = requests.post(f'{self.api_base}{api_path}', headers=headers, json=body)
            data = res.json()
        except Exception as e:
            PaymentLog.objects.create(
                payment_order=self.payment_order,
                request_payload=body,
                response_payload={'error': str(e)},
                return_code='EXCEPTION',
                return_message='Request failed',
                method=PaymentMethod.LINEPAY,
            )
            raise e

        PaymentLog.objects.create(
            payment_order=self.payment_order,
            request_payload=body,
            response_payload=data,
            return_code=data.get('returnCode', 'N/A'),
            return_message=data.get('returnMessage', 'N/A'),
            method=PaymentMethod.LINEPAY,
        )
        return data
