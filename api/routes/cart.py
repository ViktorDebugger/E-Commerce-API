from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from models.cart import Cart, CartItem
from models.product import Product
from models.user import User
from schemas.cart import CartItemCreate, CartItemUpdate, CartResponse
from api.deps import get_current_user

router = APIRouter(prefix='/cart', tags=['cart'])

def get_or_create_cart(user: User, db: Session) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if cart is None:
        cart = Cart(user_id=user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

@router.get('', response_model=CartResponse)
def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_or_create_cart(current_user, db)

@router.post('/items', response_model=CartResponse, status_code=status.HTTP_201_CREATED)
def add_item(payload: CartItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')

    cart = get_or_create_cart(current_user, db)
    item = db.query(CartItem).filter(
        CartItem.cart == cart, CartItem.product_id == payload.product_id
    ).first()

    if item:
        item.quantity += payload.quantity
    else:
        item = CartItem(cart_id=cart.id, product_id=payload.product_id, quantity=payload.quantity)
        db.add(item)

    db.commit()
    db.refresh(cart)
    return cart

@router.patch('/items/{item_id}', response_model=CartResponse)
def update_item(item_id: int, payload: CartItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = get_or_create_cart(current_user, db)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Cart item not found')

    item.quantity = payload.quantity
    db.commit()
    db.refresh(cart)
    return cart

@router.delete('/items/{item_id}', response_model=CartResponse)
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = get_or_create_cart(current_user, db)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if item is None:
            raise HTTPException(status_code=404, detail='Cart item not found')

    db.delete(item)
    db.commit()
    db.refresh(cart)
    return cart