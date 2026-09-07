import stripe
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from core.config import settings
from models.cart import Cart, CartItem
from models.order import Order, OrderItem
from models.user import User
from schemas.order import CheckoutResponse
from api.deps import get_current_user

stripe.api_key = settings.stripe_secret_key

router = APIRouter(prefix="/checkout", tags=["checkout"])


@router.post("", response_model=CheckoutResponse, status_code=status.HTTP_201_CREATED)
def checkout(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if cart is None or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = sum((item.product.price * item.quantity for item in cart.items))

    order = Order(user_id=current_user.id, total=total, status="pending")
    db.add(order)
    db.flush()

    for item in cart.items:
        db.add(OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity,
        ))

    intent = stripe.PaymentIntent.create(
        amount=int(total * 100),
        currency="usd",
         payment_method_types=["card"],
        metadata={"order_id": str(order.id)},
    )
    order.stripe_payment_intent_id = intent.id

    for item in cart.items:
        db.delete(item)

    db.commit()
    db.refresh(order)

    return CheckoutResponse(order=order, client_secret=intent.client_secret)