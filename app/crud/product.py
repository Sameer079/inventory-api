from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Product
from app.schemas import ProductCreate, ProductUpdate


def list_products(db: Session, skip: int = 0, limit: int = 50, q: str | None = None,
                  category_id: int | None = None) -> list[Product]:
    stmt = select(Product)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(Product.name.ilike(like) | Product.sku.ilike(like))
    if category_id is not None:
        stmt = stmt.where(Product.category_id == category_id)
    return list(db.scalars(stmt.order_by(Product.id).offset(skip).limit(limit)))


def get_product(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)


def get_by_sku(db: Session, sku: str) -> Product | None:
    return db.scalar(select(Product).where(Product.sku == sku))


def create_product(db: Session, data: ProductCreate) -> Product:
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, data: ProductUpdate) -> Product:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()


# TODO Day 4: list_low_stock(db)  -> products where quantity <= reorder_level
