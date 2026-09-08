from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from models.order import Order
from models.user import User
from schemas.order import OrderResponse
from api.deps import get_current_user

router = APIRouter(prefix='/orders', tags=['orders'])

@router.get('', response_model=list[OrderResponse])
def list_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Order).filter(Order.user_id == current_user.id).all()

@router.get('/{order_id}', response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.user_id == current_user.id, Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail='Order not found')
    return order