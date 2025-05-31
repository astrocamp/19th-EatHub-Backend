預約付款
Method：POST
URL：/api/payments/reserve

Request Body:
{
  "order_id": "order_123456",
  "amount": 990,
  "product_name": "premium"
}

Response:
{
  "order_id": "order_20250528_abc123",
  "payment_url_web": "https://sandbox-web-pay.line.me/payment/xxxxxx"
  "payment_url_app": "line://pay/payment/xxxxxx"
}

付款完成回傳
Method: GET
URL: /api/payments/confirm?transactionId=xxxxx&orderId=order_123456

說明：
- LINE Pay 成功付款後會自動跳轉回這個網址
- 後端會根據 transactionId 呼叫 LINE Pay Confirm API
- 若成功，更新訂單狀態為「已付款」
- 跳轉時會帶2個參數transactionId 跟 orderId

接收 Line Pay 通知
Method: POST
URL: /api/webhook

LINE Pay 付款成功後自動推送的 webhook（可搭配防火牆開放 LINE IP）
