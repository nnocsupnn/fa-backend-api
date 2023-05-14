# Financial Analysis API

> This API is created using FastAPI

<br/>

## Updating Schema using alembic

---

### Generate scripts

```bash
python -m alembic revision --autogenerate -m "commit message"
```

### Update Schema (latest generated)

```bash
python -m alembic upgrade head
```

### Start the API

```bash
pip install -r dependency.txt
```

```bash
python main.py
```

## Docker

```bash
# Create network
docker network create localdockernetwork
# Run phpmyadmin
docker run -d --name phpmyadmin --network=localdockernetwork -e PMA_HOST=mysql -e PMA_USER=root -e PMA_PORT=3306 -e PMA_PASSWORD= -p 8080:80 phpmyadmin/phpmyadmin
# Run mysql
docker run --name mysql --network=localdockernetwork --env=MYSQL_ALLOW_EMPTY_PASSWORD=yes -p 3306:3306 -d mysql
```

> visit localhost:8080
