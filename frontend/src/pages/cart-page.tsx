import { useNavigate } from "react-router-dom"
import { Minus, Plus, X } from "lucide-react"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { useCart } from "@/context/cart-context"
import { ApiError } from "@/lib/api"

export function CartPage() {
  const { cart, updateItem, removeItem } = useCart()
  const navigate = useNavigate()

  async function handleQuantityChange(itemId: number, quantity: number) {
    if (quantity < 1) return
    try {
      await updateItem(itemId, quantity)
    } catch (error) {
      const message = error instanceof ApiError ? error.detail : "Could not update quantity"
      toast.error(message)
    }
  }

  async function handleRemove(itemId: number) {
    try {
      await removeItem(itemId)
    } catch (error) {
      const message = error instanceof ApiError ? error.detail : "Could not remove item"
      toast.error(message)
    }
  }

  if (!cart || cart.items.length === 0) {
    return (
      <div className="space-y-4">
        <h1 className="text-lg font-medium">Your cart</h1>
        <p className="text-sm text-muted-foreground">Your cart is empty.</p>
        <Button variant="outline" size="sm" onClick={() => navigate("/")}>
          Browse products
        </Button>
      </div>
    )
  }

  return (
    <div className="max-w-2xl space-y-6">
      <h1 className="text-lg font-medium">Your cart</h1>

      <div className="divide-y rounded-md border">
        {cart.items.map((item) => (
          <div key={item.id} className="flex items-center justify-between gap-4 p-4">
            <div className="min-w-0">
              <p className="truncate text-sm font-medium">{item.product.name}</p>
              <p className="text-sm text-muted-foreground">${item.product.price} each</p>
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="icon"
                className="size-7"
                onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
              >
                <Minus className="size-3" />
              </Button>
              <span className="w-6 text-center text-sm">{item.quantity}</span>
              <Button
                variant="outline"
                size="icon"
                className="size-7"
                onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
              >
                <Plus className="size-3" />
              </Button>
            </div>

            <p className="w-16 text-right text-sm font-medium">${item.subtotal}</p>

            <Button
              variant="ghost"
              size="icon"
              className="size-7 text-muted-foreground"
              onClick={() => handleRemove(item.id)}
            >
              <X className="size-4" />
            </Button>
          </div>
        ))}
      </div>

      <Separator />

      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">Total</p>
        <p className="text-lg font-medium">${cart.total}</p>
      </div>

      <Button className="w-full" onClick={() => navigate("/checkout")}>
        Proceed to checkout
      </Button>
    </div>
  )
}
