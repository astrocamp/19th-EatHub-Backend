# EatHub Backend

美食行銷推薦平台。

## Dev 專案開發執行

```
docker-compose -f docker-compose.local.yml down -v
docker-compose -f docker-compose.local.yml up --build
docker-compose -f docker-compose.local.yml exec web python manage.py migrate
docker-compose -f docker-compose.local.yml exec web python manage.py createsuperuser
```

## Prod 專案執行

```
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up --build
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

## Contributor 專案開發團隊

- 張凱迪（Team Lead） [Github](https://github.com/kdchang)
- 呂亭霈 [Github](https://github.com/Ting-gif)
- 劉添順 [Github](https://github.com/skysoon1406)
- 潘奕丞 [Github](https://github.com/s30175175)
- 梁雅絜 [GitHub](https://github.com/comea22)
- 謝旻澔 [GitHub](https://github.com/qWer79790922)
