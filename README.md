# Inventory Management API

A FastAPI project built over one week. The starter covers Days 1 to 3: products and categories stored in SQLite, with tests.

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive Swagger UI.

## Test it

```bash
pytest
```

## Structure

```
app/
  main.py        app setup and routers
  database.py    engine, session, get_db dependency
  models/        SQLAlchemy tables
  schemas/       Pydantic request and response models
  crud/          database queries
  routers/       API endpoints
tests/           pytest tests
```

## Endpoints so far

| Method | Path | Purpose |
|---|---|---|
| GET | /products | List with `skip`, `limit`, `q` (name or SKU), `category_id` |
| POST | /products | Create |
| GET | /products/{id} | Fetch one |
| PUT | /products/{id} | Partial update |
| DELETE | /products/{id} | Delete |
| GET | /categories | List |
| POST | /categories | Create |

## Still to build

Search for `TODO Day` in the code. Suppliers, stock transactions, low-stock, auth and roles, Alembic, Docker.
