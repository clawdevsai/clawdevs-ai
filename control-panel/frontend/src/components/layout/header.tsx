"use client";

import { usePathname, useRouter } from "next/navigation";
import { LogOut } from "lucide-react";

const BREADCRUMBS: Record<string, string> = {
  "/": "Dashboard",
  "/agents": "Agentes",
  "/sessions": "Sessões",
  "/approvals": "Aprovações",
  "/tasks": "Tarefas",
  "/sdd": "SDD",
  "/memory": "Memória",
  "/crons": "Crons",
  "/cluster": "Cluster",
  "/settings": "Settings",
};

export function Header() {
  const pathname = usePathname();
  const router = useRouter();

  const title =
    Object.entries(BREADCRUMBS)
      .filter(([key]) => key !== "/" && pathname.startsWith(key))
      .sort((a, b) => b[0].length - a[0].length)[0]?.[1] ??
    BREADCRUMBS[pathname] ??
    "ClawDevs AI";

  function logout() {
    localStorage.removeItem("panel_token");
    router.push("/login");
  }

  return (
    <header className="h-12 flex items-center justify-between px-4 border-b border-[hsl(var(--border))] bg-[hsl(var(--card))]">
      <h1 className="text-sm font-medium text-[hsl(var(--foreground))]">
        {title}
      </h1>
      <button
        onClick={logout}
        className="flex items-center gap-1.5 text-xs text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))] transition-colors"
      >
        <LogOut size={14} />
        Sair
      </button>
    </header>
  );
}
