import { useEffect, useState } from "react"
import { Plus } from "lucide-react"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Skeleton } from "@/components/ui/skeleton"
import { ProductDialog } from "@/components/admin/product-dialog"
import { api, ApiError } from "@/lib/api"
import type { Product } from "@/types"

export function AdminProductsPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [isLoading, setIsLoading] = useState(true)

  function loadProducts() {
    setIsLoading(true)
    api
      .get<Product[]>("/products")
      .then(setProducts)
      .finally(() => setIsLoading(false))
  }

  useEffect(loadProducts, [])

  async function handleDelete(productId: number) {
    if (!confirm("Delete this product?")) return
    try {
      await api.delete(`/products/${productId}`)
      toast.success("Product deleted")
      loadProducts()
    } catch (error) {
      const message = error instanceof ApiError ? error.detail : "Could not delete product"
      toast.error(message)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-medium">Manage products</h1>
        <ProductDialog
          onSaved={loadProducts}
          trigger={
            <Button size="sm">
              <Plus className="size-4" />
              Add product
            </Button>
          }
        />
      </div>

      {isLoading ? (
        <Skeleton className="h-64" />
      ) : (
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Price</TableHead>
                <TableHead>Stock</TableHead>
                <TableHead className="w-32 text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {products.map((product) => (
                <TableRow key={product.id}>
                  <TableCell className="font-medium">{product.name}</TableCell>
                  <TableCell>${product.price}</TableCell>
                  <TableCell>{product.stock}</TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <ProductDialog
                        product={product}
                        onSaved={loadProducts}
                        trigger={
                          <Button variant="outline" size="sm">
                            Edit
                          </Button>
                        }
                      />
                      <Button
                        variant="ghost"
                        size="sm"
                        className="text-destructive"
                        onClick={() => handleDelete(product.id)}
                      >
                        Delete
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  )
}
