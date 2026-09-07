import { useEffect, useRef, useState } from "react"
import { useNavigate } from "react-router-dom"
import { Elements, PaymentElement, useElements, useStripe } from "@stripe/react-stripe-js"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { api, ApiError } from "@/lib/api"
import { stripePromise } from "@/lib/stripe"
import { useCart } from "@/context/cart-context"
import type { CheckoutResult } from "@/types"

function PaymentForm({ orderId }: { orderId: number }) {
  const stripe = useStripe()
  const elements = useElements()
  const navigate = useNavigate()
  const { refresh } = useCart()
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault()
    if (!stripe || !elements) return

    setIsSubmitting(true)
    const { error } = await stripe.confirmPayment({
      elements,
      redirect: "if_required",
    })

    if (error) {
      toast.error(error.message ?? "Payment failed")
      setIsSubmitting(false)
      return
    }

    await refresh()
    toast.success("Payment successful")
    navigate(`/orders/${orderId}`)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <PaymentElement />
      <Button type="submit" className="w-full" disabled={!stripe || isSubmitting}>
        {isSubmitting ? "Processing..." : "Pay now"}
      </Button>
    </form>
  )
}

export function CheckoutPage() {
  const [checkout, setCheckout] = useState<CheckoutResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const hasStarted = useRef(false)

  useEffect(() => {
    if (hasStarted.current) return
    hasStarted.current = true

    api
      .post<CheckoutResult>("/checkout")
      .then(setCheckout)
      .catch((err) => {
        const message = err instanceof ApiError ? err.detail : "Could not start checkout"
        setError(message)
      })
  }, [])

  if (error) {
    return <p className="text-sm text-muted-foreground">{error}</p>
  }

  if (!checkout) {
    return <Skeleton className="h-72 max-w-md" />
  }

  return (
    <div className="max-w-md space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-base font-medium">Order summary</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          {checkout.order.items.map((item) => (
            <div key={item.id} className="flex justify-between text-sm">
              <span className="text-muted-foreground">
                {item.product_name} × {item.quantity}
              </span>
              <span>${item.price}</span>
            </div>
          ))}
          <div className="flex justify-between border-t pt-2 text-sm font-medium">
            <span>Total</span>
            <span>${checkout.order.total}</span>
          </div>
        </CardContent>
      </Card>

      <Elements stripe={stripePromise} options={{ clientSecret: checkout.client_secret }}>
        <PaymentForm orderId={checkout.order.id} />
      </Elements>
    </div>
  )
}
