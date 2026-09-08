from fastapi import FastAPI
from api.routes import health, auth, products, cart, checkout, webhooks, orders

app = FastAPI(title="E-Commerce API")

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(checkout.router)
app.include_router(webhooks.router)
app.include_router(orders.router)
