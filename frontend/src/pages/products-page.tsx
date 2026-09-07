import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { toast } from "sonner"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { api, ApiError } from "@/lib/api"
import { useAuth } from "@/context/auth-context"
import { useCart } from "@/context/cart-context"
import type { Product } from "@/types"

export function ProductsPage() {
  const { user } = useAuth()
  const { addItem } = useCart()
  const [products, setProducts] = useState<Product[]>([])
  const [search, setSearch] = useState("")
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const timeout = setTimeout(() => {
      setIsLoading(true)
      const query = search ? `?search=${encodeURIComponent(search)}` : ""
      api
        .get<Product[]>(`/products${query}`)
        .then(setProducts)
        .finally(() => setIsLoading(false))
    }, 250)

    return () => clearTimeout(timeout)
  }, [search])

  async function handleAddToCart(productId: number) {
    try {
      await addItem(productId)
      toast.success("Added to cart")
    } catch (error) {
      const message = error instanceof ApiError ? error.detail : "Could not add to cart"
      toast.error(message)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <h1 className="text-lg font-medium">Products</h1>
        <Input
          placeholder="Search products..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="max-w-xs"
        />
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-40" />
          ))}
        </div>
      ) : products.length === 0 ? (
        <p className="text-sm text-muted-foreground">No products found.</p>
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {products.map((product) => (
            <Card key={product.id}>
              <CardHeader>
                <CardTitle className="text-base font-medium">
                  <Link to={`/products/${product.id}`} className="hover:underline">
                    {product.name}
                  </Link>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground line-clamp-2">
                  {product.description ?? "No description."}
                </p>
                <p className="mt-3 text-sm font-medium">${product.price}</p>
              </CardContent>
              <CardFooter>
                {user ? (
                  <Button
                    size="sm"
                    className="w-full"
                    disabled={product.stock === 0}
                    onClick={() => handleAddToCart(product.id)}
                  >
                    {product.stock === 0 ? "Out of stock" : "Add to cart"}
                  </Button>
                ) : (
                  <Button size="sm" variant="outline" className="w-full" asChild>
                    <Link to="/login">Log in to buy</Link>
                  </Button>
                )}
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
