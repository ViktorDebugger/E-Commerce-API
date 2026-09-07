import { Navigate, Outlet } from "react-router-dom"
import { useAuth } from "@/context/auth-context"

export function ProtectedRoute() {
  const { user, isLoading } = useAuth()

  if (isLoading) return null
  if (!user) return <Navigate to="/login" replace />

  return <Outlet />
}

export function AdminRoute() {
  const { user, isLoading } = useAuth()

  if (isLoading) return null
  if (!user) return <Navigate to="/login" replace />
  if (!user.is_admin) return <Navigate to="/" replace />

  return <Outlet />
}
