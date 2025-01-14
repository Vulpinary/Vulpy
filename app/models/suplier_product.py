from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models import Base

supplier_product_association_table = Table(
    "supplier_product",
    Base.metadata,
    Column("supplier_id", Integer, ForeignKey("suppliers.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
)