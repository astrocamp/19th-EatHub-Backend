Coupon API 文件
API: POST /api/v1/coupons/
一般會員 無法新增優惠券
商家 (merchant) 最多僅可新增一張未封存優惠券
VIP 商家 最多僅可新增三張未封存優惠券

Body

```json
{
  "serial_number": "TEST0000",
  "title": "滿千折百",
  "description": "單筆滿額 1000 折 100",
  "discount_type": "金額",
  "discount_value": 100,
  "total": 100,
  "started_at": "2025-06-01T00:00:00Z",
  "ended_at": "2025-06-30T23:59:59Z"
}
```

成功回應（201 Created）

```json
{
  "restaurant": {
    "name": "百味軒海鮮",
    "imageUrl": null
  },
  "discount": "100元 折價券",
  "serialNumber": "TEST0000",
  "endedAt": "2025-06-30T23:59:59Z",
  "createdAt": "2025-05-23T07:16:43.066162Z",
  "title": "滿千折百",
  "description": "單筆滿額 1000 折 100",
  "discountType": "金額",
  "discountValue": 100,
  "total": 100,
  "isArchived": false,
  "startedAt": "2025-06-01T00:00:00Z",
  "uuid": "dcffc6b2-9a1a-435d-90fe-f13589b627d9"
}
```

失敗回應

一般商家已新增過 1 張：

```json
{
  "error": "一般商家僅能擁有一張有效優惠券"
}
```

VIP 商家已新增超過 3 張：

```json
{
  "error": "VIP 商家最多只能擁有三張有效優惠券"
}
```

未登入或未提供 token：

```json
{
  "error": "未提供 Token"
}
```

欄位驗證失敗（例如折扣類型錯誤）：

```json
{
  "discount_type": ["折扣類型必須是\"金額\"或\"百分比\""]
}
```

API: PATCH /api/v1/users/:uuid/coupons/:uuid
商家/VIP 商家 (merchant) 更新使用者 coupon 狀態

Body

```json
{
  "isUsed": true
}
```

成功回應（201 Created）

```json
{
  "message": "success",
  "coupon": {
    "serialNumber": "TEST0000"
  }
}
```

失敗回應，更新失敗：

```json
{
  "error": "更新失敗"
}
```
