interface MetricsCardsProps {
  activeSessions: number
  tasksInProgress: number
  tokensConsumed: number
  failures: number
}

const cardBase =
  "rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] p-4 flex flex-col gap-2"

export function MetricsCards({
  activeSessions,
  tasksInProgress,
  tokensConsumed,
  failures,
}: MetricsCardsProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div className={cardBase}>
        <span className="text-[14px] text-[hsl(var(--muted-foreground))]">
          Active sessions
        </span>
        <span className="text-[28px] font-semibold text-white">
          {activeSessions}
        </span>
      </div>
      <div className={cardBase}>
        <span className="text-[14px] text-[hsl(var(--muted-foreground))]">
          Tasks in progress
        </span>
        <span className="text-[28px] font-semibold text-white">
          {tasksInProgress}
        </span>
      </div>
      <div className={cardBase}>
        <span className="text-[14px] text-[hsl(var(--muted-foreground))]">
          Tokens consumed
        </span>
        <span className="text-[28px] font-semibold text-white">
          {tokensConsumed.toLocaleString()}
        </span>
      </div>
      <div className={cardBase}>
        <span className="text-[14px] text-[hsl(var(--muted-foreground))]">
          Failures
        </span>
        <span className="text-[28px] font-semibold text-[#dc2828]">
          {failures}
        </span>
      </div>
    </div>
  )
}
