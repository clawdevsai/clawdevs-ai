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

"use client"

import { useEffect, useMemo, useState } from "react"
import { useQuery, useQueryClient } from "@tanstack/react-query"

import { AppLayout } from "@/components/layout/app-layout"
import { MonitoringTabs, type MonitoringTab } from "@/components/monitoring/monitoring-tabs"
import { MetricsCards } from "@/components/monitoring/metrics-cards"
import { SessionsTable } from "@/components/monitoring/sessions-table"
import { FailurePanel } from "@/components/monitoring/failure-panel"
import {
  getCycleTime,
  getFailures,
  getOverviewMetrics,
  getThroughput,
  listAgents,
  listSessions,
} from "@/lib/monitoring-api"
import { wsManager } from "@/lib/ws"
import { cn } from "@/lib/utils"

const WINDOW_OPTIONS = [30, 60, 360, 1440]

export default function MonitoringPage() {
  const queryClient = useQueryClient()
  const [activeTab, setActiveTab] = useState<MonitoringTab>("Sessions")
  const [windowMinutes, setWindowMinutes] = useState(30)
  const [showAllSessions, setShowAllSessions] = useState(false)
  const [selectedFailureId, setSelectedFailureId] = useState<string | null>(null)

  const { data: sessionsData, isLoading: sessionsLoading } = useQuery({
    queryKey: ["sessions", showAllSessions ? "all" : windowMinutes],
    queryFn: () =>
      listSessions({ windowMinutes: showAllSessions ? null : windowMinutes }),
  })

  const { data: overview } = useQuery({
    queryKey: ["overview", windowMinutes],
    queryFn: () => getOverviewMetrics({ windowMinutes }),
  })

  const { data: cycleTime } = useQuery({
    queryKey: ["cycle-time", windowMinutes],
    queryFn: () => getCycleTime({ windowMinutes }),
  })

  const { data: throughput } = useQuery({
    queryKey: ["throughput", windowMinutes],
    queryFn: () => getThroughput({ windowMinutes, groupBy: "label" }),
  })

  const { data: failures } = useQuery({
    queryKey: ["failures"],
    queryFn: () => getFailures(),
  })

  const { data: agents } = useQuery({
    queryKey: ["agents"],
    queryFn: () => listAgents(),
  })

  useEffect(() => {
    if (!wsManager) return
    const unsub = wsManager.subscribe("context-mode-metrics", (event: unknown) => {
      const e = event as { type?: string }
      if (e?.type === "context-mode-metrics") {
        queryClient.invalidateQueries({ queryKey: ["overview"] })
        queryClient.invalidateQueries({ queryKey: ["sessions"] })
      }
    })
    return unsub
  }, [queryClient])

  const activeSessions = sessionsData?.total ?? 0
  const tasksInProgress = overview?.tasks_in_progress ?? 0
  const tokensConsumed = overview?.tokens_consumed_total ?? 0
  const failureCount = failures?.total ?? 0

  const throughputItems = throughput?.items ?? []
  const agentItems = agents?.items ?? []

  const cycleAvg = cycleTime?.cycle_time_avg_seconds ?? 0
  const cycleP95 = cycleTime?.cycle_time_p95_seconds ?? 0

  const failuresList = failures?.tasks ?? []

  const windowLabel = useMemo(() => {
    if (windowMinutes === 30) return "Last 30m"
    if (windowMinutes === 60) return "Last 1h"
    if (windowMinutes === 360) return "Last 6h"
    if (windowMinutes === 1440) return "Last 24h"
    return `Last ${windowMinutes}m`
  }, [windowMinutes])

  return (
    <AppLayout>
      <div className="space-y-6 bg-[#080808] p-6 rounded-2xl">
        <div className="flex flex-col gap-3">
          <h1 className="text-[28px] font-semibold text-white">
            Monitoring Control Panel
          </h1>
          <p className="text-[16px] text-[hsl(var(--muted-foreground))]">
            Real-time operations overview and runtime controls.
          </p>
        </div>

        <MetricsCards
          activeSessions={activeSessions}
          tasksInProgress={tasksInProgress}
          tokensConsumed={tokensConsumed}
          failures={failureCount}
        />

        <div className="flex flex-wrap items-center justify-between gap-3">
          <MonitoringTabs active={activeTab} onChange={setActiveTab} />
          <div className="flex items-center gap-2">
            {WINDOW_OPTIONS.map((opt) => (
              <button
                key={opt}
                onClick={() => setWindowMinutes(opt)}
                className={cn(
                  "px-3 py-1.5 text-[14px] rounded-lg border border-[#1b1b1b]",
                  opt === windowMinutes
                    ? "bg-[#00bfff] text-black"
                    : "text-[hsl(var(--muted-foreground))] hover:text-white"
                )}
              >
                {opt === 30
                  ? "30m"
                  : opt === 60
                    ? "1h"
                    : opt === 360
                      ? "6h"
                      : "24h"}
              </button>
            ))}
          </div>
        </div>

        {activeTab === "Sessions" && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-[20px] font-semibold text-white">Sessions</h2>
                <p className="text-[14px] text-[hsl(var(--muted-foreground))]">
                  {showAllSessions ? "All sessions" : windowLabel}
                </p>
              </div>
              <button
                onClick={() => setShowAllSessions((prev) => !prev)}
                className="text-[14px] text-[#00bfff]"
              >
                {showAllSessions ? "Show recent" : "Show all"}
              </button>
            </div>
            <SessionsTable
              items={sessionsData?.items ?? []}
              isLoading={sessionsLoading}
            />
          </div>
        )}

        {activeTab === "Tasks" && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] p-4">
                <p className="text-[14px] text-[hsl(var(--muted-foreground))]">
                  Cycle time average
                </p>
                <p className="text-[20px] font-semibold text-white">
                  {cycleAvg.toFixed(0)}s
                </p>
              </div>
              <div className="rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] p-4">
                <p className="text-[14px] text-[hsl(var(--muted-foreground))]">
                  Cycle time p95
                </p>
                <p className="text-[20px] font-semibold text-white">
                  {cycleP95.toFixed(0)}s
                </p>
              </div>
            </div>

            <div className="rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] p-4">
              <h3 className="text-[16px] font-semibold text-white">
                Throughput by label
              </h3>
              <div className="mt-3 space-y-2 text-[14px]">
                {throughputItems.length === 0 ? (
                  <p className="text-[hsl(var(--muted-foreground))]">
                    No throughput data yet.
                  </p>
                ) : (
                  throughputItems.map((item) => (
                    <div
                      key={item.group}
                      className="flex items-center justify-between border-b border-[#1b1b1b] pb-2"
                    >
                      <span className="text-white">{item.group}</span>
                      <span className="text-[hsl(var(--muted-foreground))]">
                        {item.completed_count}
                      </span>
                    </div>
                  ))
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div className="rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] p-4">
                <h3 className="text-[16px] font-semibold text-white">Failures</h3>
                <div className="mt-3 space-y-2 text-[14px]">
                  {failuresList.length === 0 ? (
                    <p className="text-[hsl(var(--muted-foreground))]">
                      No failures detected in the current window.
                    </p>
                  ) : (
                    failuresList.map((task) => (
                      <button
                        key={task.id}
                        onClick={() => setSelectedFailureId(task.id)}
                        className={cn(
                          "w-full text-left rounded-lg border border-[#1b1b1b] px-3 py-2",
                          selectedFailureId === task.id
                            ? "bg-[#dc2828]/20 text-white"
                            : "text-[hsl(var(--muted-foreground))] hover:text-white"
                        )}
                      >
                        <div className="flex items-center justify-between">
                          <span>{task.title}</span>
                          <span>{task.failure_count}x</span>
                        </div>
                        <div className="text-[12px] opacity-70 mt-1">
                          {task.last_error ?? "No error recorded"}
                        </div>
                      </button>
                    ))
                  )}
                </div>
              </div>
              <FailurePanel taskId={selectedFailureId} />
            </div>
          </div>
        )}

        {activeTab === "Agents" && (
          <div className="rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] p-4">
            <h3 className="text-[16px] font-semibold text-white">Agents</h3>
            <div className="mt-3 space-y-2 text-[14px]">
              {agentItems.length === 0 ? (
                <p className="text-[hsl(var(--muted-foreground))]">
                  No agents available.
                </p>
              ) : (
                agentItems.map((agent) => (
                  <div
                    key={agent.id}
                    className="flex items-center justify-between border-b border-[#1b1b1b] pb-2"
                  >
                    <span className="text-white">{agent.display_name}</span>
                    <span className="text-[hsl(var(--muted-foreground))]">
                      {agent.status}
                    </span>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {activeTab === "Metrics" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] p-4">
              <p className="text-[14px] text-[hsl(var(--muted-foreground))]">
                Tokens avg per task
              </p>
              <p className="text-[20px] font-semibold text-white">
                {overview?.tokens_consumed_avg_per_task?.toFixed(1) ?? "0"}
              </p>
            </div>
            <div className="rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] p-4">
              <p className="text-[14px] text-[hsl(var(--muted-foreground))]">
                Backlog count
              </p>
              <p className="text-[20px] font-semibold text-white">
                {overview?.backlog_count ?? 0}
              </p>
            </div>
            <div className="rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] p-4">
              <p className="text-[14px] text-[hsl(var(--muted-foreground))]">
                Tasks completed
              </p>
              <p className="text-[20px] font-semibold text-white">
                {overview?.tasks_completed ?? 0}
              </p>
            </div>
            <div className="rounded-xl border border-[#1b1b1b] bg-[#0f0f0f] p-4">
              <p className="text-[14px] text-[hsl(var(--muted-foreground))]">
                Tasks in review
              </p>
              <p className="text-[20px] font-semibold text-white">
                {overview?.open_tasks ?? 0}
              </p>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  )
}
