from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from app.models.seller import Seller
from app.models.category import Category
from app.models.supplier import Supplier
from app.models.product import Product




