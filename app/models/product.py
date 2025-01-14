from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base
from app.models.suplier_product import supplier_product_association_table



class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    seller = relationship("Seller", back_populates="products")
    category = relationship("Category", back_populates="products")
    suppliers = relationship(
        "Supplier",
        secondary=supplier_product_association_table,
        back_populates="products",
        lazy="dynamic"
    )