最新動態與優惠券清單

GET /api/v1/merchant/promotions-coupons/ 

```python

API = {
    "result": {
        "restaurant": {
            "name": "麵屋武藏 本店",
            "uuid": "8eb03a32-d421-4c41-a614-fdf0fa9ea651"
        }
        "promotions": [
            {
            "title": "週年慶活動",
            "description": string,
            "created_at":"2025-05-12T12:34:56Z",
            "started_at": "2025-05-15T12:34:56Z",
            "ended_at": "2025-05-15T12:34:56Z",
            "image_url": string | null,
            "uuid": "d123e456-78ab-90cd-ef12-345678901234"
             },
        ]
        "coupons": [
            {
            "serial_number": "ABC123XYZ",
            "created_at":"2025-05-15T12:34:56Z",
            "started_at": "2025-05-15T12:34:56Z",
            "ended_at": "2025-05-15T12:34:56Z",
            "title": "買一送一",
            "description": "限內用，僅限週末使用",
            "discount": string,
            "total": 100,
            "uuid": "f234e567-89bc-01de-gh23-456789012345",
            "redeemed_count": 42,
            "used_count": 18,
           
            } 
        ]          
    }
}
```


POST /api/v1/merchant/promotions/<uuid:uuid>/archive/
POST /api/v1/merchant/coupons/<uuid:uuid>/archive/







