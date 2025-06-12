# EatHub Backend

美食行銷推薦平台。

## 專案開發執行

請參閱 Makefile，本機開發和測試：

```
make up env=local
make down env=local
docker-compose -f docker-compose.local.yml exec -it web pytest
```

```
docker-compose -f docker-compose.local.yml exec web python manage.py migrate
docker-compose -f docker-compose.local.yml exec web python manage.py createsuperuser
docker-compose -f docker-compose.local.yml exec web python manage.py collectstatic
```

## 專案部署執行

```
make up env=prod
make down env=prod
```

```
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic
```

## Contributor 專案開發團隊

- 張凱迪（Team Lead） [Github](https://github.com/kdchang)
- 呂亭霈 [Github](https://github.com/Ting-gif)
- 劉添順 [Github](https://github.com/skysoon1406)
- 潘奕丞 [Github](https://github.com/s30175175)
- 梁雅絜 [GitHub](https://github.com/comea22)
- 謝旻澔 [GitHub](https://github.com/qWer79790922)
