from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Supplier, Category
from app.models.product import Product
from app.models.seller import Seller

from app.schemas.product import ProductSchema, ProductCreate, ProductUpdateSchema
from app.services.auth import get_current_seller

product_router = APIRouter(prefix="/products", tags=["Products"])

@product_router.get("/", response_model=list[ProductSchema])
def get_products(db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    products = db.query(Product).filter(Product.seller_id == current_seller.id).all()
    return [ProductSchema.from_orm(product) for product in products]

@product_router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate, db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    try:
        suppliers = db.query(Supplier).filter(Supplier.id.in_(product_data.supplier_ids)).all()
        new_product = Product(
            **product_data.dict(exclude={"supplier_ids"}),
            seller_id=current_seller.id,
            suppliers=suppliers
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return ProductSchema.from_orm(new_product)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Database error: {e}") from e
    except NoResultFound as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Supplier not found: {e}") from e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected server error: {e}") from e

@product_router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@product_router.put("/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
def update_product(
        product_id: int,
        product: ProductUpdateSchema,
        db: Session = Depends(get_db),
        current_seller: Seller = Depends(get_current_seller)
):
    try:
        db_product = db.query(Product).filter(Product.id == product_id, Product.seller_id == current_seller.id).first()
        if not db_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        db.commit()
        db.refresh(db_product)
        return ProductSchema.from_orm(db_product)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Database error: {e}") from e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected server error: {e}") from e

@product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    try:
        product = db.query(Product).filter(Product.id == product_id, Product.seller_id == current_seller.id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        db.delete(product)
        db.commit()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected server error: {e}") from e