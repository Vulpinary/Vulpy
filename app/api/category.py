import logging

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models import Category, Seller
from app.schemas.category import CategorySchema, CategoryCreate
from app.services.auth import get_current_seller
from app.database import get_db

logger = logging.getLogger(__name__)

category_router = APIRouter(prefix="/categories", tags=["Categories"])

@category_router.get("/", response_model=list[CategorySchema])
def get_categories(db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    try:
        categories = db.query(Category).all()
        return categories
    except Exception as e:
        logger.exception(f"Error retrieving categories: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve categories") from e


@category_router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    try:
        new_category = Category(name=category_data.name, seller_id=current_seller.id)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except IntegrityError as e:
        db.rollback()  # Rollback transaction on error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category creation failed: {e}") from e
    except Exception as e:
        db.rollback()
        logger.exception(f"Error creating category: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create category") from e

@category_router.get("/{category_id}", response_model=CategorySchema)
def get_category(category_id: int, db: Session = Depends(get_db)):
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return CategorySchema.from_orm(category)
    except Exception as e:
        logger.exception(f"Error retrieving category: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve category") from e

@category_router.put("/{category_id}", response_model=CategorySchema, status_code=status.HTTP_200_OK)
def update_category(category_id: int, category_data: CategoryCreate, db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    try:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        db_category.name = category_data.name
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category update failed: {e}") from e
    except Exception as e:
        db.rollback()
        logger.exception(f"Error updating category: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update category") from e

@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        db.delete(category)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.exception(f"Error deleting category: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete category") from e