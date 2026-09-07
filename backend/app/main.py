from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import health, auth, products, cart, checkout, webhooks, orders

app = FastAPI(title="E-Commerce API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(checkout.router)
app.include_router(webhooks.router)
app.include_router(orders.router)