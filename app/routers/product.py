from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db


router = APIRouter(tags=["products"])

#get all products
@router.get("/products")
def get_products(db: Session = Depends(get_db)):

    products = db.query(models.Product).all()
    return products

#get product by id
@router.get("/product/{id}")
def get_product(id: int, db: Session = Depends(get_db)):

    product = db.query(models.Product).filter(models.Product.id == id).first()
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id {id} does not exists")
    
    return product

#create new product
@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductResponse)
def create_product(new_product: schemas.CreateProduct, db: Session = Depends(get_db)):

    product_dict = new_product.model_dump()
    product = models.Product(**product_dict)
    db.add(product)
    db.commit()
    db.refresh(product)

    return product

#delete product
@router.delete("/product/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    product = db.query(models.Product).filter(models.Product.id == id)

    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id: {id} does not exists")

    product.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update product
@router.put("/product/{id}")
def update_product(id: int, product: schemas.UpdateProduct, db: Session = Depends(get_db)):

    product_query = db.query(models.Product).filter(models.Product.id == id)

    if not product_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id: {id} does not exists")

    product_query.update(product.model_dump(), synchronize_session=False)
    db.commit()

    return product_query.first()
