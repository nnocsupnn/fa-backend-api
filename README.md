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
