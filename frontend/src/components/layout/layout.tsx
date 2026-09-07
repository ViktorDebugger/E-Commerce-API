import { Outlet } from "react-router-dom"
import { Header } from "@/components/layout/header"

export function Layout() {
  return (
    <div className="flex min-h-svh flex-col">
      <Header />
      <main className="mx-auto w-full max-w-5xl flex-1 px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}
