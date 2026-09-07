import { Routes, Route } from "react-router-dom"
import { Layout } from "@/components/layout/layout"
import { ProtectedRoute, AdminRoute } from "@/components/protected-route"
import { LoginPage } from "@/pages/login-page"
import { SignupPage } from "@/pages/signup-page"
import { ProductsPage } from "@/pages/products-page"
import { ProductDetailPage } from "@/pages/product-detail-page"
import { CartPage } from "@/pages/cart-page"
import { CheckoutPage } from "@/pages/checkout-page"
import { OrdersPage } from "@/pages/orders-page"
import { OrderDetailPage } from "@/pages/order-detail-page"
import { AdminProductsPage } from "@/pages/admin-products-page"

export function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<ProductsPage />} />
        <Route path="products/:id" element={<ProductDetailPage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="signup" element={<SignupPage />} />

        <Route element={<ProtectedRoute />}>
          <Route path="cart" element={<CartPage />} />
          <Route path="checkout" element={<CheckoutPage />} />
          <Route path="orders" element={<OrdersPage />} />
          <Route path="orders/:id" element={<OrderDetailPage />} />
        </Route>

        <Route element={<AdminRoute />}>
          <Route path="admin/products" element={<AdminProductsPage />} />
        </Route>
      </Route>
    </Routes>
  )
}
