我的收藏清單（查詢登入使用者已收藏的餐廳）

GET /api/v1/favorites/

Cookie: auth_token={user_uuid}:{token}

Success Response [200 OK]:
"""
[
  {
    "uuid": "fda8fabc-1234-4567-89ab-1234567890ab",
    "restaurant_uuid": "9abcfabc-4567-4567-89ab-abcdef123456",
    "created_at": "2025-05-17T09:00:00Z"
  }
]
"""
Error Response [401 Unauthorized]:
	未提供 token
	Token 無效或過期

收藏餐廳

POST /api/v1/restaurants/{uuid}/favorite/

Cookie:	auth_token={user_uuid}:{token}

Success Response [201 Created]:
"""
{
  "success": true
}
"""
Error Response [400 Bad Request]:
	該餐廳已經收藏過

Error Response [401 Unauthorized]:
	未登入

取消收藏

DELETE /api/v1/restaurants/{uuid}/favorite/

Cookie:	auth_token={user_uuid}:{token}

Success Response [204 No Content]:
"""
{
  "success": true
}
"""
Error Response [200 OK]:
	該餐廳沒有收藏紀錄（也會回 success: false）

Error Response [401 Unauthorized]:
	未登入
