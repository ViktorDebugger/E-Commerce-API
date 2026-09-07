export interface User {
  id: number
  email: string
  is_admin: boolean
}

export interface Product {
  id: number
  name: string
  description: string | null
  price: string
  stock: number
}

export interface CartItem {
  id: number
  product: Product
  quantity: number
  subtotal: string
}

export interface Cart {
  id: number
  items: CartItem[]
  total: string
}

export interface OrderItem {
  id: number
  product_name: string
  price: string
  quantity: number
}

export interface Order {
  id: number
  status: string
  total: string
  created_at: string
  items: OrderItem[]
}

export interface CheckoutResult {
  order: Order
  client_secret: string
}
