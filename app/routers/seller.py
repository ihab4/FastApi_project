from typing import List

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(tags=["sellers"])

@router.post("/seller", status_code=status.HTTP_201_CREATED, response_model=schemas.SellerResponse)
def create_product(new_seller: schemas.CreateSeller, db: Session = Depends(get_db)):

    hached_password = utils.get_password_hash(new_seller.password)
    new_seller.password = hached_password

    seller_dict = new_seller.model_dump()

    seller = models.Seller(**seller_dict)
    db.add(seller)
    db.commit()
    db.refresh(seller)

    return seller

@router.get("/sellers", response_model=List[schemas.SellerResponse])
def get_sellers(db: Session = Depends(get_db)):
    sellers = db.query(models.Seller).all()

    return sellers

@router.get("/seller/{id}", response_model=schemas.SellerResponse)
def get_seller(id: int, db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.id == id).first()

    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"seller with id {id} does not exist")
    
    return seller

@router.put("/seller/{id}", response_model=schemas.SellerResponse)
def update_seller(id: int, seller: schemas.CreateSeller, db: Session = Depends(get_db)):
    seller_query = db.query(models.Seller).filter(models.Seller.id == id)

    if not seller_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"seller with id {id} does not exist")
    
    seller_query.update(seller.model_dump(), synchronize_session=False)

    db.commit()

    return seller_query.first()

@router.put("/password/{id}")
def change_password(id: int, seller: schemas.ChangePassword, db: Session = Depends(get_db)):
    seller_query = db.query(models.Seller).filter(models.Seller.id == id)

    if not seller_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"seller with id {id} does not exist")
    
    seller_query.update(seller.model_dump(), synchronize_session=False)

    db.commit()

    return seller_query.first()

@router.delete("/seller/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_seller(id: int, db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.id == id)

    if not seller.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"seller with id {id} does not exist")
    
    seller.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
