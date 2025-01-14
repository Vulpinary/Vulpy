import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.models.seller import Seller
from app.schemas.seller import SellerCreate, SellerSchema, SellerUpdate, SellerAuth
from app.services.auth import get_current_seller
from app.database import get_db
from app.services.product_service import authenticate_seller, create_seller

router = APIRouter(prefix="/sellers", tags=["Sellers"])

@router.get("/", response_model=list[SellerSchema])
def get_sellers(db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    sellers = db.query(Seller).all()
    return sellers

@router.get("/{seller_id}", response_model=SellerSchema)
def get_seller(seller_id: int, db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    seller = db.query(Seller).filter(Seller.id == seller_id).first()
    if seller is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
    return seller

@router.post("/register", response_model=SellerSchema, status_code=status.HTTP_201_CREATED)
def register_seller(seller_create: SellerCreate, db: Session = Depends(get_db)):
    try:
        return create_seller(db, seller_create)
    except Exception as e:
        logging.exception(f"Error registering seller: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error registering seller")

@router.post("/login", response_model=SellerSchema)
def login_seller(seller_auth: SellerAuth, db: Session = Depends(get_db)):
    try:
        return authenticate_seller(db, seller_auth, db)
    except HTTPException as e:
        logging.exception(f"Error authenticating seller: {e}")
        raise e

@router.put("/{seller_id}", response_model=SellerSchema)
def update_seller(seller_id: int, seller_data: SellerUpdate, db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    if seller_id != current_seller.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    seller = db.query(Seller).get(seller_id)
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
    for key, value in seller_data.dict(exclude_unset=True).items():
        setattr(seller, key, value)
    try:
        db.commit()
        db.refresh(seller)
        return seller
    except Exception as e:
        db.rollback()
        logging.exception(f"Error updating seller: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating seller")

@router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_seller(seller_id: int, db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    if seller_id != current_seller.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    seller = db.query(Seller).get(seller_id)
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
    try:
        db.delete(seller)
        db.commit()
    except Exception as e:
        db.rollback()
        logging.exception(f"Error deleting seller: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting seller")