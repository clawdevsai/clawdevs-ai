import { useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { getFailureDetail } from "@/lib/monitoring-api"

interface FailurePanelProps {
  taskId: string | null
}

export function FailurePanel({ taskId }: FailurePanelProps) {
  const [expanded, setExpanded] = useState(false)

  const { data, isLoading } = useQuery({
    queryKey: ["failure-detail", taskId],
    queryFn: () => (taskId ? getFailureDetail(taskId) : Promise.resolve(null)),
    enabled: Boolean(taskId),
  })

  if (!taskId) {
    return (
      <div className="rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] p-4 text-sm text-[hsl(var(--muted-foreground))]">
        Select a failed task to inspect details.
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] p-4 text-sm text-[hsl(var(--muted-foreground))]">
        Loading failure detail...
      </div>
    )
  }

  const message = data?.message ?? "No failure message recorded."

  return (
    <div className="rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] p-4 space-y-3">
      <div>
        <p className="text-[14px] text-[hsl(var(--muted-foreground))]">Message</p>
        <p className="text-[16px] text-white">{message}</p>
      </div>
      <button
        onClick={() => setExpanded((prev) => !prev)}
        className="text-[14px] text-[#00bfff]"
      >
        {expanded ? "Hide details" : "Show stack trace & evidence"}
      </button>
      {expanded && (
        <div className="space-y-3">
          <div>
            <p className="text-[14px] text-[hsl(var(--muted-foreground))]">
              Stack trace
            </p>
            <pre className="mt-2 whitespace-pre-wrap text-[14px] text-[#d4d4d4] bg-[#080808] border border-[#1b1b1b] rounded-lg p-3">
              {data?.stack_trace ?? "No stack trace captured."}
            </pre>
          </div>
          <div>
            <p className="text-[14px] text-[hsl(var(--muted-foreground))]">
              Evidence
            </p>
            <ul className="mt-2 text-[14px] text-white space-y-1">
              {data?.evidence?.length ? (
                data.evidence.map((item, idx) => <li key={idx}>{item}</li>)
              ) : (
                <li className="text-[hsl(var(--muted-foreground))]">
                  No evidence attached.
                </li>
              )}
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}
