import logging

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app import product_router, get_db
from app.api import seller
from app.api.category import category_router
from app.api.supplier import supplier_router
from app.schemas.seller import Token

from app.services.auth import create_access_token
from fastapi import FastAPI, Depends
from app.config.config import Settings
from app.services.product_service import authenticate_seller

settings_instance = Settings()
engine = create_engine(settings_instance.DATABASE_URL, echo=settings_instance.DATABASE_ECHO)

app = FastAPI()

app.include_router(product_router)
app.include_router(category_router)
app.include_router(seller.router)
app.include_router(supplier_router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        logging.info("Starting login process...")
        logging.info(f"Form data received: {form_data}")
        logging.info("Calling authenticate_seller...")
        seller = await authenticate_seller(form_data, db)
        logging.info(f"authenticate_seller returned: {seller}")
        if not seller:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        logging.info("Calling create_access_token...")
        access_token = await create_access_token(data={"sub": seller.username, "seller_id": seller.id}, db=db)
        logging.info(f"create_access_token returned: {access_token}")
        logging.info("Login successful.")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        logging.error(f"HTTPException during login: {e}")
        raise e
    except Exception as e:
        logging.exception(f"Unexpected error during login: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error during login") from e



