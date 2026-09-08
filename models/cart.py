from sqlalchemy import ForeignKey, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)

    items: Mapped[list['CartItem']] = relationship(back_populates='cart', cascade='all, delete-orphan')

class CartItem(Base):
    __tablename__ = 'cart_items'
    __table_args__ = (UniqueConstraint('cart_id', 'product_id', name='uq_cart_products'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    cart: Mapped['Cart'] = relationship(back_populates='items')
    product: Mapped['Product'] = relationship()