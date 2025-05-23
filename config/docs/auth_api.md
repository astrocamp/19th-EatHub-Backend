註冊新會員。
POST /api/v1/auth/signup

Request Body :
{
    'firstname':'T'
    'lastname':'ex3'
    'username':'text3'
    'email':'text3@example.com'
    'password':'text323'
}

Success Respones [201 Created]:
{
    'message':'註冊成功',
    'user':{
        'uuid':"ec13b219-xxxx-xxxx-xxxx-abcdef123456",
        'userName':'text3',
        'email':'text3@example.com'
    }
}

Error Respones [400 Bad Request]:
    -欄位格式錯誤
    -email已存在


登入會員，驗證email、密碼，成功後回傳認證 Cookie。
POST /api/v1/auth/login

Request Body :
{
    "email": "user@example.com",
    "password": "your-password"
}

Success Respones [200 OK]:
{
    'firstName':'t',
    'lastName':'ext3',
    'userName':'text3'
    'message':'登入成功'
}

Cookie:
    - 名稱：'auth_token'
    - 格式：'{user_uuid}:{token}'
    - 屬性：HttpOnly, Secure, SameSite=Lax
    - 有效時間：3600 秒（1 小時）

Error Respones [400 Bad Request]:
    -欄位空白
Error Respones [401 Unauthorized]:
    -密碼錯誤
Error Respones [404 Not Found]:
    -使用者不存在


認證方式。
GET /api/v1/auth/me

    -從 Cookie 中自動讀取 'auth_token'
    -格式 '{user_uuid}:{token}'

Success Respones [200 OK]:
{
    'message': '驗證成功 {user_uuid}'
}

Error Respones [401 Unauthorized]:
    -未提供 Token
    -Token 驗證失敗


登出目前登入使用者，清除認證用的 Cookie 、 Cache 中的 Token。
POST /api/v1/auth/logout


Cookie:
    -'auth_token':'{user_uuid}:{token}'

Success Respones [200 OK]:
{
    'message': '登出成功'
}
    -Cookie 'auth_token' 刪除
    -Cache key 'user_token:{user_uuid}' 清除

Error Respones [400 Bad Request]:
    -未提供 Token
response
{
    message:登出成功
    or reeor:未提供 Token / 400
}


註冊新商家。
POST /api/v1/auth/merchant/signup/

Request Body :
{
    'userName':'text3'
    'email':'text3@example.com'
    'password':'text323'
    'role':'merchant'
}

Success Respones [201 Created]:
{
    'message':'商家註冊成功',
    'user':{
        'uuid':"ec13b219-xxxx-xxxx-xxxx-abcdef123456",
        'userName':'text3',
        'email':'text3@example.com',
        'role':'merchant'
    }
}

Error Respones [400 Bad Request]:
    -欄位格式錯誤
    -email已存在