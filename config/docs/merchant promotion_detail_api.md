Method：POST
URL：/api/v1/promotions/
權限：僅限登入的餐廳帳戶使用
內容格式：multipart/form-data

Request Body :
{
    'title'：字數255 /必填,
    'description'：/非必填,
    'started_at'：使用 ISO 格式 /非必填,
    'ended_at'：使用 ISO 格式 /非必填,
    'image_url'：JPG/PNG/HEIC 限制 1MB 以內 /非必填,
}
備註：
    使用multipart/form-data傳送資料
    image_url實際會由後端上傳並轉為 URL 儲存

限制條件：
    一般商家：1則
    VIP商家：3則
嘗試超出上限時，API拒絕建立動態訊息，回傳403

Success Respones [201 Created]:
{
    "uuid": "ed07f9ea-98c7-43d9-93a0-b9e9e1ab2b3a",
    "title": "夏季優惠大放送",
    "description": "指定套餐買一送一！",
    "started_at": "2025-06-01T00:00:00Z",
    "ended_at": "2025-06-15T23:59:59Z",
    "image_url": "https://res.cloudinary.com/xxx/promo1.jpg",
    "created_at": "2025-05-23T12:00:00Z"
}

Error Respones [404 Not Found]:
    -"title": ["此欄位為必填。"]
    -"image": ["圖片太大，請小於 1MB"]
Error Respones [403 Forbidden]:
    -"error": "請使用餐廳帳戶登入。"
    -"error": "非 VIP 商家最多只能建立 1 則活動"
    -"error": "VIP 商家最多只能建立 3 則活動"