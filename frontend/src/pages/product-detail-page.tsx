import { useEffect, useState } from "react"
import { Link, useNavigate, useParams } from "react-router-dom"
import { toast } from "sonner"
import { ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { api, ApiError } from "@/lib/api"
import { useAuth } from "@/context/auth-context"
import { useCart } from "@/context/cart-context"
import type { Product } from "@/types"

export function ProductDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const { addItem } = useCart()
  const [product, setProduct] = useState<Product | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    api
      .get<Product>(`/products/${id}`)
      .then(setProduct)
      .catch(() => setProduct(null))
      .finally(() => setIsLoading(false))
  }, [id])

  async function handleAddToCart() {
    if (!product) return
    try {
      await addItem(product.id)
      toast.success("Added to cart")
    } catch (error) {
      const message = error instanceof ApiError ? error.detail : "Could not add to cart"
      toast.error(message)
    }
  }

  if (isLoading) {
    return <Skeleton className="h-64 max-w-lg" />
  }

  if (!product) {
    return (
      <div className="space-y-4">
        <p className="text-sm text-muted-foreground">Product not found.</p>
        <Button variant="outline" size="sm" onClick={() => navigate("/")}>
          Back to products
        </Button>
      </div>
    )
  }

  return (
    <div className="max-w-lg space-y-6">
      <Link to="/" className="flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground">
        <ArrowLeft className="size-4" />
        Back to products
      </Link>

      <div className="space-y-2">
        <h1 className="text-xl font-medium">{product.name}</h1>
        <p className="text-lg font-medium text-muted-foreground">${product.price}</p>
      </div>

      <p className="text-sm leading-relaxed">{product.description ?? "No description available."}</p>

      <p className="text-sm text-muted-foreground">
        {product.stock > 0 ? `${product.stock} in stock` : "Out of stock"}
      </p>

      {user ? (
        <Button disabled={product.stock === 0} onClick={handleAddToCart}>
          {product.stock === 0 ? "Out of stock" : "Add to cart"}
        </Button>
      ) : (
        <Button variant="outline" asChild>
          <Link to="/login">Log in to buy</Link>
        </Button>
      )}
    </div>
  )
}
