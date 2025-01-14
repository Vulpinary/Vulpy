from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models import Base
from app.models.suplier_product import supplier_product_association_table


class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False, index=True)
    seller = relationship("Seller", back_populates="suppliers")
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=False)
    address = Column(String(500), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    category = relationship("Category", backref="suppliers")
    products = relationship(
        "Product",
        secondary=supplier_product_association_table,
        back_populates="suppliers",
        lazy="dynamic"
    )