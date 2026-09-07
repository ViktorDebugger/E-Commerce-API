import { useEffect, useState } from "react"
import { Link, useParams } from "react-router-dom"
import { ArrowLeft } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Skeleton } from "@/components/ui/skeleton"
import { api } from "@/lib/api"
import type { Order } from "@/types"

export function OrderDetailPage() {
  const { id } = useParams()
  const [order, setOrder] = useState<Order | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    api
      .get<Order>(`/orders/${id}`)
      .then(setOrder)
      .catch(() => setOrder(null))
      .finally(() => setIsLoading(false))
  }, [id])

  if (isLoading) {
    return <Skeleton className="h-64 max-w-lg" />
  }

  if (!order) {
    return <p className="text-sm text-muted-foreground">Order not found.</p>
  }

  return (
    <div className="max-w-lg space-y-6">
      <Link to="/orders" className="flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground">
        <ArrowLeft className="size-4" />
        Back to orders
      </Link>

      <div className="flex items-center justify-between">
        <h1 className="text-lg font-medium">Order #{order.id}</h1>
        <Badge variant={order.status === "paid" ? "default" : "secondary"}>{order.status}</Badge>
      </div>

      <p className="text-sm text-muted-foreground">
        Placed on {new Date(order.created_at).toLocaleString()}
      </p>

      <div className="divide-y rounded-md border">
        {order.items.map((item) => (
          <div key={item.id} className="flex justify-between p-4 text-sm">
            <span>
              {item.product_name} × {item.quantity}
            </span>
            <span>${item.price}</span>
          </div>
        ))}
      </div>

      <div className="flex justify-between text-sm font-medium">
        <span>Total</span>
        <span>${order.total}</span>
      </div>
    </div>
  )
}
