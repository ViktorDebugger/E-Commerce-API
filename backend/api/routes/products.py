from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from api.deps import get_current_admin_user

router = APIRouter(prefix='/products', tags=['products'])

@router.get('', response_model=list[ProductResponse])
def list_products(search: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Product)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    return query.all()

@router.get('/{product_id}', response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return product

@router.post('', response_model=ProductResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_current_admin_user)])
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.patch('/{product_id}', response_model=ProductResponse,
              dependencies=[Depends(get_current_admin_user)])
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

@router.delete('/{product_id}',
               dependencies=[Depends(get_current_admin_user)],
               status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')

    db.delete(product)
    db.commit()