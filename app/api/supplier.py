from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.seller import Seller
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierSchema, SupplierUpdate
from app.services.auth import get_current_seller

supplier_router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@supplier_router.post("/", response_model=SupplierSchema, status_code=status.HTTP_201_CREATED)
async def create_supplier(supplier_data: SupplierCreate, db: Session = Depends(get_db)):
    try:
      new_supplier = Supplier(**supplier_data.dict())
      db.add(new_supplier)
      db.commit()
      db.refresh(new_supplier)
      return SupplierSchema.from_orm(new_supplier)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating supplier: {e}") from e

@supplier_router.get("/", response_model=List[SupplierSchema]) # Added GET route for /suppliers
async def get_suppliers(db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    suppliers = db.query(Supplier).filter(Supplier.seller_id == current_seller.id).all()
    return suppliers

@supplier_router.get("/{supplier_id}", response_model=SupplierSchema)
async def get_supplier(supplier_id: int, db: Session = Depends(get_db),
                       current_seller: Seller = Depends(get_current_seller)):
    # Находим поставщика по ID
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id, Supplier.seller_id == current_seller.id).first()

    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")

    # Преобразуем поставщика в SupplierSchema и возвращаем
    return SupplierSchema.from_orm(supplier)

@supplier_router.put("/{supplier_id}", response_model=SupplierSchema)
def update_supplier(supplier_id: int, supplier_data: SupplierUpdate, db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id, Supplier.seller_id == current_seller.id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    for key, value in supplier_data.dict(exclude_unset=True).items():
        setattr(supplier, key, value)
    db.commit()
    db.refresh(supplier)
    return SupplierSchema.from_orm(supplier)

@supplier_router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id, Supplier.seller_id == current_seller.id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db.delete(supplier)
    db.commit()