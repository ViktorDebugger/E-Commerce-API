import stripe
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from core.config import settings
from models.order import Order

router = APIRouter(prefix='/webhooks', tags=['webhooks'])

@router.post('/stripe')
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.stripe_webhook_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=400, detail='Invalid webhook signature')

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        order = db.query(Order).filter(Order.stripe_payment_intent_id == intent['id']).first()
        if order:
            order.status = 'paid'
            db.commit()

    return {'status': 'received'}