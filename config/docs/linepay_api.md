本模組提供以下主要功能：
取得訂閱產品列表（GET /api/v1/payments/products/）
發起 LINE Pay 訂閱付款（POST /api/v1/payments/subscription/）
處理 LINE Pay 付款完成導向（GET/POST /api/v1/payments/linepay/confirm/）

GET /api/v1/payments/products/
說明： 取得所有訂閱產品方案
權限：需登入商家
回傳：uuid, name, plan_type, amount, interval_days

POST /api/v1/payments/subscription/
說明： 發起 LINE Pay 訂閱付款請求，並產生付款訂單
權限：需登入商家
Request Body:
{
  "product_id": "cb5e8317-fbd8-402c-ab12-bd332b63ca11",
  "amount": 10690
}

Response:
{
  "order_id": "order_20250601_XXXXXXX",
  "payment_url_web": "https://...",
  "payment_url_app": "line://..."
}

Error Respones [400 BadRrequest]:
    -金額不正確
    -缺少參數
Error Respones [404 Not Found]:
    -找不到使用者
    -找不到產品


GET/POST /api/v1/payments/linepay/confirm/
說明： LINE Pay 付款完成後，使用者導向此 confirmUrl，由伺服器驗證交易並建立訂閱

{
  "orderId": "order_20250601_XXXXXXX",
  "transactionId": 20250601XXXXXXXX
}

Response:
{
  "message": "付款確認成功", 
  "transactionId": "20250601XXXXXXXX"
  }

Error Respones [400 BadRrequest]:
    -缺少參數
Error Respones [404 Not Found]:
    -找不到訂單

備註:
confirmUrl 必須與 LINE PAY Channel 設定一致。
若訂閱尚未到期，僅能於結束前 7 天內續約。
所有交易皆紀錄至 PaymentLog，利於日後追蹤。
