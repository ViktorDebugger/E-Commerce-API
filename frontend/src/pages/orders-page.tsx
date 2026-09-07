import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { Badge } from "@/components/ui/badge"
import { Skeleton } from "@/components/ui/skeleton"
import { api } from "@/lib/api"
import type { Order } from "@/types"

export function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    api
      .get<Order[]>("/orders")
      .then(setOrders)
      .finally(() => setIsLoading(false))
  }, [])

  return (
    <div className="max-w-2xl space-y-6">
      <h1 className="text-lg font-medium">Your orders</h1>

      {isLoading ? (
        <div className="space-y-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-16" />
          ))}
        </div>
      ) : orders.length === 0 ? (
        <p className="text-sm text-muted-foreground">You haven't placed any orders yet.</p>
      ) : (
        <div className="divide-y rounded-md border">
          {orders.map((order) => (
            <Link
              key={order.id}
              to={`/orders/${order.id}`}
              className="flex items-center justify-between p-4 hover:bg-muted/50"
            >
              <div>
                <p className="text-sm font-medium">Order #{order.id}</p>
                <p className="text-sm text-muted-foreground">
                  {new Date(order.created_at).toLocaleDateString()}
                </p>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-sm font-medium">${order.total}</span>
                <Badge variant={order.status === "paid" ? "default" : "secondary"}>
                  {order.status}
                </Badge>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
