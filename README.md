# Financial Analysis API

> This API is created using FastAPI

<br/>

## Updating Schema using alembic

---

### Start the API

```bash
pip install -r dependency.txt
```

```bash
python main.py
```

> You can set specific port by adding `--port` argument in cli.

```bash
python main.py --port 3000
```

## Once application is running, visit API Docs.

> localhost/api/docs

<br/>

## Docker

```bash
# Create network
docker network create localdockernetwork
# Run phpmyadmin
docker run -d --name phpmyadmin --network=localdockernetwork -e PMA_HOST=mysql -e PMA_USER=root -e PMA_PORT=3306 -e PMA_PASSWORD= -p 8080:80 phpmyadmin/phpmyadmin
# Run mysql
docker run --name mysql --network=localdockernetwork --env=MYSQL_ALLOW_EMPTY_PASSWORD=yes -p 3306:3306 -d mysql
```
