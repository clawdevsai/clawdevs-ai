/* 
 * Copyright (c) 2026 Diego Silva Morais <lukewaresoftwarehouse@gmail.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { getApiBaseUrl } from "@/lib/api-base-url";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch(
        `${getApiBaseUrl()}/auth/login`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        }
      );
      if (!res.ok) {
        setError("Usuário ou senha incorretos");
        return;
      }
      const data = await res.json();
      localStorage.setItem("panel_token", data.access_token);
      router.push("/");
    } catch {
      setError("Erro de conexão com o servidor");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[hsl(var(--background))]">
      <div className="w-full max-w-sm space-y-8 p-8 rounded-xl border border-[hsl(var(--border))] bg-[hsl(var(--card))]">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-[hsl(var(--primary))]">
            ClawDevs AI
          </h1>
          <p className="text-sm text-[hsl(var(--muted-foreground))] mt-1">
            Control Panel
          </p>
        </div>
        <form onSubmit={handleLogin} className="space-y-4" data-testid="login-form">
          <div>
            <label className="block text-sm font-medium mb-1">Usuário</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 rounded-md bg-[hsl(var(--input))] border border-[hsl(var(--border))] text-sm focus:outline-none focus:ring-1 focus:ring-[hsl(var(--ring))]"
              required
              data-testid="login-username"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Senha</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 rounded-md bg-[hsl(var(--input))] border border-[hsl(var(--border))] text-sm focus:outline-none focus:ring-1 focus:ring-[hsl(var(--ring))]"
              required
              data-testid="login-password"
            />
          </div>
          {error && (
            <p className="text-sm text-[hsl(var(--destructive))]" data-testid="login-error">{error}</p>
          )}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 px-4 rounded-md bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] font-medium text-sm hover:opacity-90 disabled:opacity-50 transition-opacity"
            data-testid="login-submit"
          >
            {loading ? "Entrando..." : "Entrar"}
          </button>
        </form>
      </div>
    </div>
  );
}
