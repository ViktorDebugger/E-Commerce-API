import { createContext, useContext, useEffect, useState, type ReactNode } from "react"
import { api } from "@/lib/api"
import type { User } from "@/types"

interface AuthContextValue {
  user: User | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  signup: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem("token")
    if (!token) {
      setIsLoading(false)
      return
    }

    api
      .get<User>("/auth/me")
      .then(setUser)
      .catch(() => localStorage.removeItem("token"))
      .finally(() => setIsLoading(false))
  }, [])

  async function login(email: string, password: string) {
    const { access_token } = await api.post<{ access_token: string }>("/auth/login", {
      email,
      password,
    })
    localStorage.setItem("token", access_token)
    const me = await api.get<User>("/auth/me")
    setUser(me)
  }

  async function signup(email: string, password: string) {
    await api.post("/auth/signup", { email, password })
    await login(email, password)
  }

  function logout() {
    localStorage.removeItem("token")
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error("useAuth must be used within AuthProvider")
  return ctx
}
