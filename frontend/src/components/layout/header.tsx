import { Link, useNavigate } from "react-router-dom"
import { ShoppingCart, User as UserIcon } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { useAuth } from "@/context/auth-context"
import { useCart } from "@/context/cart-context"

export function Header() {
  const { user, logout } = useAuth()
  const { cart } = useCart()
  const navigate = useNavigate()

  const itemCount = cart?.items.reduce((sum, item) => sum + item.quantity, 0) ?? 0

  function handleLogout() {
    logout()
    navigate("/")
  }

  return (
    <header className="border-b">
      <div className="mx-auto flex h-14 max-w-5xl items-center justify-between px-4">
        <Link to="/" className="text-sm font-medium tracking-tight">
          E-Commerce API
        </Link>

        <nav className="flex items-center gap-1">
          <Button variant="ghost" size="sm" asChild>
            <Link to="/">Products</Link>
          </Button>

          {user && (
            <Button variant="ghost" size="sm" asChild>
              <Link to="/orders">Orders</Link>
            </Button>
          )}

          {user?.is_admin && (
            <Button variant="ghost" size="sm" asChild>
              <Link to="/admin/products">Admin</Link>
            </Button>
          )}

          {user && (
            <Button variant="ghost" size="sm" asChild className="relative">
              <Link to="/cart">
                <ShoppingCart className="size-4" />
                {itemCount > 0 && (
                  <span className="absolute -right-1 -top-1 flex size-4 items-center justify-center rounded-full bg-foreground text-[10px] text-background">
                    {itemCount}
                  </span>
                )}
              </Link>
            </Button>
          )}

          {user ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm">
                  <UserIcon className="size-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuLabel className="font-normal text-muted-foreground">
                  {user.email}
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout}>Log out</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <>
              <Button variant="ghost" size="sm" asChild>
                <Link to="/login">Log in</Link>
              </Button>
              <Button size="sm" asChild>
                <Link to="/signup">Sign up</Link>
              </Button>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}
