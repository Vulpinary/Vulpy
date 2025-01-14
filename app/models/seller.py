from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models import Base

class Seller(Base):
    __tablename__ = "sellers"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    products = relationship("Product", back_populates="seller")
    suppliers = relationship("Supplier", back_populates="seller")
    categories = relationship("Category", back_populates="seller")
