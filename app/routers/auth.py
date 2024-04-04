from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import models, schemas, utils, oauth2
from ..database import get_db


router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(login_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    seller = db.query(models.Seller).filter(models.Seller.email == login_credentials.username).first()

    if not seller:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    if not utils.verify_password(login_credentials.password, seller.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    
    access_token = oauth2.create_access_token(data={"user_id": str(seller.id)})

    return {"access_token": access_token, "token_type": "bearer"}
