from decimal import Decimal

from db.session import SessionLocal
from models.user import User
from models.product import Product
from core.security import hash_password

PRODUCTS = [
    {"name": "Wireless Mouse", "description": "Ergonomic wireless mouse with USB receiver", "price": Decimal("24.99"), "stock": 50},
    {"name": "Mechanical Keyboard", "description": "Tactile mechanical keyboard, RGB backlit", "price": Decimal("79.99"), "stock": 30},
    {"name": "USB-C Hub", "description": "7-in-1 USB-C hub with HDMI and card reader", "price": Decimal("34.50"), "stock": 40},
    {"name": "Webcam 1080p", "description": "Full HD webcam with built-in microphone", "price": Decimal("49.99"), "stock": 25},
    {"name": "Laptop Stand", "description": "Adjustable aluminum laptop stand", "price": Decimal("29.99"), "stock": 60},
]

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "adminpass123"


def seed():
    db = SessionLocal()
    try:
        if db.query(Product).count() == 0:
            for data in PRODUCTS:
                db.add(Product(**data))
            print(f"Seeded {len(PRODUCTS)} products.")
        else:
            print("Products already exist, skipping.")

        admin = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if admin is None:
            admin = User(
                email=ADMIN_EMAIL,
                hashed_password=hash_password(ADMIN_PASSWORD),
                is_admin=True,
            )
            db.add(admin)
            print(f"Seeded admin user: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
        else:
            print("Admin user already exists, skipping.")

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
