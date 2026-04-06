import { formatDistanceToNow } from "date-fns"

import type { SessionItem } from "@/lib/monitoring-api"

interface SessionsTableProps {
  items: SessionItem[]
  isLoading: boolean
}

export function SessionsTable({ items, isLoading }: SessionsTableProps) {
  if (isLoading) {
    return (
      <div className="rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] p-4 text-sm text-[hsl(var(--muted-foreground))]">
        Loading sessions...
      </div>
    )
  }

  if (items.length === 0) {
    return (
      <div className="rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] p-6 text-center">
        <p className="text-[20px] font-semibold text-white">No recent sessions</p>
        <p className="text-[16px] text-[hsl(var(--muted-foreground))] mt-2">
          Sessions will appear here once the runtime starts. Check back after your
          next run.
        </p>
      </div>
    )
  }

  return (
    <div className="rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] overflow-hidden">
      <table className="w-full text-left text-[14px]">
        <thead className="bg-[#101010] text-[hsl(var(--muted-foreground))]">
          <tr>
            <th className="px-4 py-3">Session</th>
            <th className="px-4 py-3">Agent</th>
            <th className="px-4 py-3">Status</th>
            <th className="px-4 py-3">Messages</th>
            <th className="px-4 py-3">Tokens</th>
            <th className="px-4 py-3">Last active</th>
          </tr>
        </thead>
        <tbody className="text-white">
          {items.map((item) => (
            <tr key={item.id} className="border-t border-[#1b1b1b]">
              <td className="px-4 py-3">{item.session_label}</td>
              <td className="px-4 py-3">{item.agent_slug ?? "—"}</td>
              <td className="px-4 py-3 capitalize">{item.status}</td>
              <td className="px-4 py-3">{item.message_count}</td>
              <td className="px-4 py-3">{item.token_count}</td>
              <td className="px-4 py-3 text-[hsl(var(--muted-foreground))]">
                {item.last_active_at
                  ? formatDistanceToNow(new Date(item.last_active_at), {
                      addSuffix: true,
                    })
                  : "—"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
