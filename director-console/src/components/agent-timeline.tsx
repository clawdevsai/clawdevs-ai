"use client";

import type { TimelineBucket } from "@/lib/server/types";

type AgentTimelineProps = {
  buckets: TimelineBucket[];
};

export function AgentTimeline({ buckets }: AgentTimelineProps) {
  return (
    <div className="bg-white shadow-sm border border-slate-200 rounded-3xl p-6">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-slate-900 tracking-tight">Timeline por agente</h2>
        <p className="mt-1 text-sm text-slate-500 font-medium">Ultimos eventos destacados por origem do stream.</p>
      </div>
      {buckets.length === 0 ? (
        <p className="text-sm font-medium text-slate-500">Nenhuma timeline disponivel.</p>
      ) : (
        <div className="grid gap-5 md:grid-cols-2">
          {buckets.map((bucket) => (
            <div key={bucket.agent} className="rounded-2xl border border-slate-100 bg-slate-50 p-5 hover:shadow-sm transition duration-200">
              <div className="text-sm font-bold text-slate-900 flex items-center gap-2 border-b border-slate-200 pb-3">
                <div className="w-2 h-2 rounded-full bg-indigo-500 relative"><div className="absolute inset-0 bg-indigo-500 rounded-full animate-ping opacity-20"></div></div>
                {bucket.agent}
              </div>
              <div className="mt-4 space-y-4 text-sm text-slate-600">
                {bucket.items.length === 0 ? (
                  <div className="text-xs font-medium text-slate-500">Nenhum evento recente.</div>
                ) : (
                  bucket.items.map((item) => (
                    <div key={`${bucket.agent}-${item.stream}-${item.id}`} className="border-l-2 border-slate-200 pl-4 py-1 relative">
                      <div className="absolute w-2.5 h-2.5 bg-slate-300 rounded-full -left-[6px] top-1.5 border-2 border-slate-50"></div>
                      <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">{item.timestamp}</div>
                      <div className="font-semibold text-slate-800">{item.eventName}</div>
                      {item.issueId ? <div className="mt-1.5 flex"><span className="text-[10px] font-bold text-indigo-700 bg-indigo-50 border border-indigo-100 rounded-md px-2 py-0.5">Issue: {item.issueId}</span></div> : null}
                    </div>
                  ))
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
