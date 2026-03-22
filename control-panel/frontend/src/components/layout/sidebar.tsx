"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  Bot,
  MessageSquare,
  ShieldCheck,
  CheckSquare,
  FileText,
  Brain,
  Clock,
  Server,
  Settings,
} from "lucide-react";

const NAV_ITEMS = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/agents", label: "Agentes", icon: Bot },
  { href: "/sessions", label: "Sessões", icon: MessageSquare },
  { href: "/approvals", label: "Aprovações", icon: ShieldCheck },
  { href: "/tasks", label: "Tarefas", icon: CheckSquare },
  { href: "/sdd", label: "SDD", icon: FileText },
  { href: "/memory", label: "Memória", icon: Brain },
  { href: "/crons", label: "Crons", icon: Clock },
  { href: "/cluster", label: "Cluster", icon: Server },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-56 shrink-0 h-screen flex flex-col border-r border-[hsl(var(--border))] bg-[hsl(var(--card))]">
      {/* Logo */}
      <div className="p-4 border-b border-[hsl(var(--border))]">
        <div className="flex items-center gap-2">
          <span className="text-[hsl(var(--primary))] font-bold text-lg">
            ClawDevs
          </span>
          <span className="text-[hsl(var(--muted-foreground))] text-xs">
            AI
          </span>
        </div>
        <p className="text-xs text-[hsl(var(--muted-foreground))] mt-0.5">
          Control Panel
        </p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-2 space-y-0.5 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive =
            item.href === "/"
              ? pathname === "/"
              : pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors",
                isActive
                  ? "bg-[hsl(var(--primary)/0.15)] text-[hsl(var(--primary))] font-medium"
                  : "text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))] hover:bg-[hsl(var(--secondary))]"
              )}
            >
              <Icon size={16} />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
