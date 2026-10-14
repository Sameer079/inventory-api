from fastapi import FastAPI

from app import models  # noqa: F401  (registers tables on Base)
from app.database import Base, engine
from app.routers import categories, products

# Day 6: replace create_all with Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Management API", version="0.1.0")

app.include_router(products.router)
app.include_router(categories.router)

# TODO Day 4: stock router (/stock/in, /stock/out) and suppliers router
# TODO Day 5: auth router (/auth/register, /auth/login)


@app.get("/", tags=["Health"])
def health():
    return {"status": "ok"}
