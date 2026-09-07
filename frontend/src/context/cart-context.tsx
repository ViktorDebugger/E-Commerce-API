import { createContext, useContext, useCallback, useEffect, useState, type ReactNode } from "react"
import { api } from "@/lib/api"
import { useAuth } from "@/context/auth-context"
import type { Cart } from "@/types"

interface CartContextValue {
  cart: Cart | null
  isLoading: boolean
  refresh: () => Promise<void>
  addItem: (productId: number, quantity?: number) => Promise<void>
  updateItem: (itemId: number, quantity: number) => Promise<void>
  removeItem: (itemId: number) => Promise<void>
}

const CartContext = createContext<CartContextValue | null>(null)

export function CartProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth()
  const [cart, setCart] = useState<Cart | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const refresh = useCallback(async () => {
    if (!user) {
      setCart(null)
      return
    }
    setIsLoading(true)
    try {
      const data = await api.get<Cart>("/cart")
      setCart(data)
    } finally {
      setIsLoading(false)
    }
  }, [user])

  useEffect(() => {
    refresh()
  }, [refresh])

  async function addItem(productId: number, quantity = 1) {
    const data = await api.post<Cart>("/cart/items", { product_id: productId, quantity })
    setCart(data)
  }

  async function updateItem(itemId: number, quantity: number) {
    const data = await api.patch<Cart>(`/cart/items/${itemId}`, { quantity })
    setCart(data)
  }

  async function removeItem(itemId: number) {
    const data = await api.delete<Cart>(`/cart/items/${itemId}`)
    setCart(data)
  }

  return (
    <CartContext.Provider value={{ cart, isLoading, refresh, addItem, updateItem, removeItem }}>
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  const ctx = useContext(CartContext)
  if (!ctx) throw new Error("useCart must be used within CartProvider")
  return ctx
}
