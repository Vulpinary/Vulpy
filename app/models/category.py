from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    products = relationship("Product", back_populates="category")
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    seller = relationship("Seller", back_populates="categories")